import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const stories = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/stories' }),
  schema: z.object({
    title: z.string(),
    titleZh: z.string(),
    dynasty: z.string(),
    era: z.string(),
    source: z.string(),
    sourceZh: z.string(),
    author: z.string().default('Unknown'),
    compiled: z.string().default(''),
    tags: z.array(z.string()).default([]),
    excerpt: z.string(),
    featured: z.boolean().default(false),
    order: z.number().default(99),
    published: z.coerce.date(),
    image: z.string().optional(),
    imageAlt: z.string().default(''),
    original: z.string().default(''),
    originalNote: z.string().default(''),
    notes: z
      .array(
        z.object({
          term: z.string(),
          text: z.string(),
        })
      )
      .default([]),
    related: z.array(z.string()).default([]),
  }),
});

const worldview = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/worldview' }),
  schema: z.object({
    title: z.string(),
    titleZh: z.string(),
    branch: z.enum(['cosmology', 'beings', 'figures', 'cultivation']),
    summary: z.string(),
    order: z.number().default(99),
    image: z.string().optional(),
    imageAlt: z.string().default(''),
    related: z.array(z.string()).default([]),
  }),
});

const features = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/features' }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string().default(''),
    excerpt: z.string(),
    published: z.coerce.date(),
    order: z.number().default(99),
    image: z.string().optional(),
    imageAlt: z.string().default(''),
    related: z.array(z.string()).default([]),
  }),
});

const guides = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    order: z.number().default(1),
    published: z.coerce.date(),
    image: z.string().optional(),
  }),
});

export const collections = { stories, worldview, features, guides };
