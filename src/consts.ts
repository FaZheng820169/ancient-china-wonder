export const SITE = {
  name: 'Ancient China Wonder',
  shortName: 'ACW',
  tagline: 'A universe of gods, ghosts, fox spirits and wonders from ancient China',
  description:
    'Ancient China Wonder collects, translates and systematises classical Chinese zhiguai — tales of the strange — into one coherent fantasy universe: gods, immortals, ghosts, fox spirits, monsters and the underworld.',
  url: 'https://ancient-chinawonder.vercel.app',
  author: 'Ancient China Wonder',
  locale: 'en',
};

export const NAV = [
  { href: '/stories', label: 'Stories' },
  { href: '/worldview', label: 'Worldview' },
  { href: '/features', label: 'Features' },
  { href: '/guides', label: 'Guides' },
  { href: '/start-here', label: 'Start Here' },
  { href: '/about', label: 'About' },
];

export const TAG_LABELS: Record<string, string> = {
  'Fox Spirit': 'Fox Spirit',
  Ghost: 'Ghost',
  Immortal: 'Immortal',
  Monster: 'Monster',
  Deity: 'Deity',
  Underworld: 'Underworld',
  Sword: 'Sword & Heroism',
  Love: 'Love',
  Justice: 'Justice & Karma',
  Trickster: 'Trickery',
  Transformation: 'Transformation',
  Dreams: 'Dreams',
};

export const BRANCHES = {
  cosmology: {
    label: 'Cosmos & Geography',
    zh: '宇宙与地理',
    blurb:
      'How the world is built: the three realms, Mount Kunlun, the isles of Penglai, the Nine Provinces, and the Courts of the Dead beneath the earth.',
  },
  beings: {
    label: 'Races & Beings',
    zh: '种族与生灵',
    blurb:
      'Gods, immortals, humans, ghosts, fox spirits, nature sprites, monstrous beasts and dragons — and the rules that separate them.',
  },
  figures: {
    label: 'Figures',
    zh: '人物图鉴',
    blurb:
      'The recurring cast of the universe: the Queen Mother of the West, Nie Yinniang, Nie Xiaoqian, Lü Dongbin and others.',
  },
  cultivation: {
    label: 'Cultivation & Rules',
    zh: '修炼体系',
    blurb:
      'How a human becomes an immortal, how an animal becomes a spirit, what a tribulation is, and how cause and effect bind everything together.',
  },
} as const;
