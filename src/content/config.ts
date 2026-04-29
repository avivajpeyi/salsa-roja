import { z, defineCollection } from 'astro:content';

const moves = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    youtube_id: z.string(),
    youtube_url: z.string().url(),
    title: z.string(),
    tags: z.array(z.string()),
    status: z.enum(['new', 'reviewing', 'learned']).default('new'),
    date_added: z.coerce.date(),
  }),
});

export const collections = { moves };
