"""The package's import layering, read from the source so it stays that way.

- The schedule vocabulary lives in `pdf_extract.model`, at the bottom.
- The pipeline (everything but the labeler, the evals, the factory and the
  CLI that wires them together) never imports those three.
- No two modules import each other, directly or through others, counting
  imports made inside functions: those must not be a way around a cycle.
"""

from __future__ import annotations

import ast
from functools import cache
from pathlib import Path

PACKAGE = "pdf_extract"
SRC = Path(__file__).resolve().parents[1] / "src" / PACKAGE

# Packages above the pipeline, which the pipeline must not import.
TOOLS = ("labeling", "evals", "factory")
# The command line imports every part of the package.
CLI = f"{PACKAGE}.__main__"
# Cycles that predate the check, each broken by an import inside a function.
KNOWN_CYCLES = {
    frozenset({f"{PACKAGE}.factory.sandbox", f"{PACKAGE}.factory.workspace"}),
}


@cache
def _modules() -> dict[str, Path]:
    out = {}
    for path in SRC.rglob("*.py"):
        parts = [PACKAGE, *path.relative_to(SRC).with_suffix("").parts]
        if parts[-1] == "__init__":
            parts.pop()
        out[".".join(parts)] = path
    return out


def _is_type_checking(node: ast.If) -> bool:
    return "TYPE_CHECKING" in ast.unparse(node.test)


def _imports(module: str) -> list[tuple[str, str | None]]:
    """(module imported, name imported from it or None) for every runtime import."""
    tree = ast.parse(_modules()[module].read_text(encoding="utf-8"))
    found: list[tuple[str, str | None]] = []
    stack: list[ast.AST] = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, ast.If) and _is_type_checking(node):
            stack.extend(node.orelse)
            continue
        if isinstance(node, ast.Import):
            found += [(a.name, None) for a in node.names if a.name.split(".")[0] == PACKAGE]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            if node.module.split(".")[0] == PACKAGE:
                found += [(node.module, a.name) for a in node.names]
        stack.extend(ast.iter_child_nodes(node))
    return found


def _resolve(name: str) -> str:
    modules = _modules()
    while name not in modules:
        name = name.rpartition(".")[0]
    return name


@cache
def _graph() -> dict[str, frozenset[str]]:
    modules = _modules()
    graph = {}
    for module in modules:
        targets = set()
        for imported, name in _imports(module):
            submodule = f"{imported}.{name}"
            targets.add(submodule if submodule in modules else _resolve(imported))
        targets.discard(module)
        graph[module] = frozenset(targets)
    return graph


def _in(module: str, package: str) -> bool:
    return module == package or module.startswith(f"{package}.")


def test_the_pipeline_does_not_import_the_labeler_evals_or_factory():
    tools = [f"{PACKAGE}.{tool}" for tool in TOOLS]
    wrong = sorted(
        f"{module} imports {target}"
        for module, targets in _graph().items()
        if module != CLI and not any(_in(module, tool) for tool in tools)
        for target in targets
        if any(_in(target, tool) for tool in tools)
    )
    assert wrong == []


def test_the_model_imports_only_timeparse():
    assert _graph()[f"{PACKAGE}.model"] <= {f"{PACKAGE}.timeparse"}


def test_the_vocabulary_is_imported_from_the_model_not_from_labels():
    model = ast.parse(_modules()[f"{PACKAGE}.model"].read_text(encoding="utf-8"))
    vocabulary = {
        node.name for node in model.body
        if isinstance(node, ast.FunctionDef | ast.ClassDef)
    } | {
        target.id for node in model.body if isinstance(node, ast.Assign)
        for target in node.targets if isinstance(target, ast.Name)
    }
    wrong = sorted(
        f"{module} imports {name} from {imported}"
        for module in _modules()
        for imported, name in _imports(module)
        if _in(imported, f"{PACKAGE}.labeling") and name in vocabulary
    )
    assert wrong == []


def test_no_module_imports_itself_through_others():
    graph = _graph()
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    cycles: list[frozenset[str]] = []

    def visit(module: str) -> None:  # Tarjan's strongly connected components
        index[module] = low[module] = len(index)
        stack.append(module)
        for target in graph[module]:
            if target not in index:
                visit(target)
                low[module] = min(low[module], low[target])
            elif target in stack:
                low[module] = min(low[module], index[target])
        if low[module] == index[module]:
            component = set()
            while True:
                member = stack.pop()
                component.add(member)
                if member == module:
                    break
            if len(component) > 1:
                cycles.append(frozenset(component))

    for module in sorted(graph):
        if module not in index:
            visit(module)
    assert sorted(sorted(c) for c in cycles if c not in KNOWN_CYCLES) == []
