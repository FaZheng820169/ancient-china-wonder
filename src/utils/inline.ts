/**
 * Minimal inline-emphasis renderer for plain-text frontmatter fields.
 *
 * Astro renders a bare `{value}` as escaped text, so Markdown written inside
 * fields such as `notes[].text` or `originalNote` would otherwise display its
 * asterisks literally (they are not passed through the Markdown pipeline the
 * way a story's body is). This converts `**strong**` and `*emphasis*` into real
 * elements so the two can be written the same way everywhere.
 *
 * Input is escaped first, so it is safe to pass to `set:html`.
 */
export function inline(text: string | undefined | null): string {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}
