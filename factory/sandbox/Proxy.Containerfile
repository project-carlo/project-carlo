# Stripe smokescreen v0.1.0, built locally to avoid the failing GHCR pull.
# Release checksums: https://github.com/stripe/smokescreen/releases/download/v0.1.0/SHA256SUMS
# Changing this file produces a new carlo-egress:<hash> image.
FROM docker.io/library/alpine:3.20 AS download
RUN case "$(uname -m)" in \
        x86_64) arch=amd64; checksum=4e1e447449e3cc653dae956208588722b5c8fe8ce894f633adc756a851d1ec46 ;; \
        aarch64) arch=arm64; checksum=f15ddd0dc2b2cbc6d7318f441928939eb9bedfab2a1881508af3096a1e24b7c9 ;; \
        *) exit 1 ;; \
    esac \
    && wget -O /tmp/smokescreen.tar.gz "https://github.com/stripe/smokescreen/releases/download/v0.1.0/smokescreen_v0.1.0_linux_${arch}.tar.gz" \
    && echo "${checksum}  /tmp/smokescreen.tar.gz" | sha256sum -c - \
    && mkdir /out \
    && tar -xzf /tmp/smokescreen.tar.gz -C /out --strip-components=1

FROM docker.io/library/alpine:3.20
COPY --from=download /out/smokescreen /usr/local/bin/smokescreen
USER 65532:65532
EXPOSE 4750
ENTRYPOINT ["/usr/local/bin/smokescreen"]
