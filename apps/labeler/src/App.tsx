import { useEffect, useState } from "react";
import { api } from "./api";
import { useRoute } from "./lib/route";
import type { Config } from "./types";
import { BulletinPage } from "./views/BulletinPage";
import { QueuePage } from "./views/QueuePage";

const LABELER_KEY = "labeler:name";

export function App() {
  const route = useRoute();
  const [config, setConfig] = useState<Config | null>(null);
  const [labeler, setLabeler] = useState(() => localStorage.getItem(LABELER_KEY) ?? "");

  useEffect(() => {
    api
      .config()
      .then((c) => {
        setConfig(c);
        setLabeler((current) => current || c.default_labeler);
      })
      .catch(() => setConfig(null));
  }, []);

  const changeLabeler = (name: string) => {
    setLabeler(name);
    localStorage.setItem(LABELER_KEY, name);
  };

  if (route.page === "bulletin") {
    return (
      <BulletinPage
        parish={route.parish}
        hash={route.hash}
        config={config}
        labeler={labeler}
        onLabelerChange={changeLabeler}
      />
    );
  }
  return <QueuePage config={config} labeler={labeler} onLabelerChange={changeLabeler} />;
}
