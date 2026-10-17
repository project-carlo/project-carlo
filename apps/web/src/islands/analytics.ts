/**
 * The analytics every prerendered page loads (see src/lib/analytics.ts): its
 * pageview, and the links it marks for tracking. The app's own pages start
 * analytics in main.tsx instead.
 */
import { startAnalytics, trackPageview } from "../lib/analytics";

startAnalytics();
trackPageview();
