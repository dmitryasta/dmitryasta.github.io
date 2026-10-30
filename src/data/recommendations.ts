// Real LinkedIn recommendations go here ONLY after they were read on the profile and the author's consent is clear.
// Until then the site links to LinkedIn and shows no quotations.
export interface Recommendation { text: string; author: string; role: string; date?: string; url: string }
export const RECOMMENDATIONS: Record<'en' | 'ru' | 'sr', Recommendation[]> = { en: [], ru: [], sr: [] };
