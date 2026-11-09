// Real LinkedIn recommendations go here ONLY after they were read on the profile and the author's consent is clear.
// State on 2026-11-08: the public LinkedIn profile shows no recommendations, so the list is empty by design.
// The home page then shows only the "Professional profile" block with the link to LinkedIn. Never add invented or paraphrased quotations.
export interface Recommendation { text: string; author: string; role: string; date?: string; url: string }
export const RECOMMENDATIONS: Record<'en' | 'ru' | 'sr', Recommendation[]> = { en: [], ru: [], sr: [] };
