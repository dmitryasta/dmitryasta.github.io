import { en, type UI } from './en';
import { ru } from './ru';
import { sr } from './sr';
import type { Lang } from '../lib/pages';

export type { UI };
export const UIS: Record<Lang, UI> = { en, ru, sr };
export const ui = (lang: Lang): UI => UIS[lang];

/** Escape HTML and turn **bold** into <strong>. Used for short UI strings only. */
export function inline(text: string): string {
  const esc = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return esc.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}

/** Build-time guard: RU and SR must have exactly the same keys and array lengths as EN. */
function shape(v: unknown, path = ''): string[] {
  if (Array.isArray(v)) return [`${path}[${v.length}]`, ...(v.length ? shape(v[0], path + '[]') : [])];
  if (v && typeof v === 'object') return Object.entries(v as object).flatMap(([k, x]) => shape(x, `${path}.${k}`));
  return [`${path}:${typeof v}`];
}
export function assertParity(): void {
  const base = shape(en);
  for (const l of ['ru', 'sr'] as const) {
    const other = shape(UIS[l]);
    const missing = base.filter((x) => !other.includes(x));
    const extra = other.filter((x) => !base.includes(x));
    if (missing.length || extra.length) {
      throw new Error(`i18n parity error in ${l}: missing ${missing.slice(0, 5).join(', ')} extra ${extra.slice(0, 5).join(', ')}`);
    }
  }
}
