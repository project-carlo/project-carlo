import {
  OG_IMAGE_ALT,
  OG_IMAGE_HEIGHT,
  OG_IMAGE_PATH,
  OG_IMAGE_WIDTH,
  SITE_LOCALE,
  SITE_NAME,
  absoluteUrl,
  serializeJsonLd,
} from "../lib/seo";

interface StaticHeadProps {
  title: string;
  description: string;
  canonicalUrl: string;
  /** JSON-LD nodes, emitted as one `<script type="application/ld+json">`. */
  jsonLd: unknown;
  cssPath: string;
  fontPaths: string[];
}

/**
 * The full `<head>` of a prerendered page: title, description, canonical,
 * Open Graph / Twitter tags, JSON-LD, font preloads and the stylesheet.
 */
export function StaticHead({
  title,
  description,
  canonicalUrl,
  jsonLd,
  cssPath,
  fontPaths,
}: StaticHeadProps) {
  const origin = new URL(canonicalUrl).origin;
  const ogImageUrl = absoluteUrl(origin, OG_IMAGE_PATH);
  return (
    <head>
      <meta charSet="UTF-8" />
      <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0, viewport-fit=cover"
      />
      <meta name="description" content={description} />
      <meta name="theme-color" content="#F3ECD8" />
      <meta name="color-scheme" content="light" />
      <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
      <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
      <link rel="manifest" href="/site.webmanifest" />
      <link rel="canonical" href={canonicalUrl} />
      <title>{title}</title>

      <meta property="og:type" content="website" />
      <meta property="og:site_name" content={SITE_NAME} />
      <meta property="og:locale" content={SITE_LOCALE} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:image" content={ogImageUrl} />
      <meta property="og:image:width" content={String(OG_IMAGE_WIDTH)} />
      <meta property="og:image:height" content={String(OG_IMAGE_HEIGHT)} />
      <meta property="og:image:alt" content={OG_IMAGE_ALT} />

      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImageUrl} />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: serializeJsonLd(jsonLd) }}
      />
      {fontPaths.map((fp) => (
        <link
          key={fp}
          rel="preload"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
          href={fp}
        />
      ))}
      <link rel="stylesheet" href={cssPath} />
    </head>
  );
}
