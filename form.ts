// Enquiry form configuration.
//
// The form sends to Formspree (https://formspree.io), which forwards each enquiry by email to the
// address set in the Formspree form settings. The form ID was created by the site owner in Formspree
// (2026-11-08). If the value is empty or does not look like a Formspree form URL, the form shows an
// "unavailable" message and does not pretend to send anything.
//
// How to set the endpoint (any ONE of these):
//   1. Edit FORM_ENDPOINT below, e.g.  'https://formspree.io/f/abcdwxyz'
//   2. Or set the build variable PUBLIC_FORM_ENDPOINT (GitHub: Settings, Secrets and variables,
//      Actions, Variables, name FORM_ENDPOINT, and the workflow passes it as PUBLIC_FORM_ENDPOINT).
//
// The endpoint is public by design (it is visible in the page source of any form). It contains
// no password or key.

export const FORM_ENDPOINT = 'https://formspree.io/f/mbggewvd';

const PATTERN = /^https:\/\/formspree\.io\/f\/[A-Za-z0-9]{6,}$/;

/** Returns the endpoint, or an empty string when none is set or the value does not look like a Formspree form URL. */
export function formEndpoint(): string {
  const fromEnv = ((import.meta.env.PUBLIC_FORM_ENDPOINT as string | undefined) || '').trim();
  const value = fromEnv || FORM_ENDPOINT.trim();
  return PATTERN.test(value) ? value : '';
}

export const TOPICS = ['market-entry', 'distributors', 'import-export', 'representation', 'research', 'automation', 'other'] as const;
export type Topic = (typeof TOPICS)[number];

/** Which topic of the form matches each service page. */
export const SERVICE_TOPIC: Record<string, Topic> = {
  'serbia-market-entry': 'market-entry',
  'find-distributors-in-serbia': 'distributors',
  'import-to-serbia': 'import-export',
  'export-from-serbia': 'import-export',
  'local-commercial-representation': 'representation',
  'serbia-market-research': 'research',
  'business-automation': 'automation',
};
