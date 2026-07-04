import {create} from 'zustand';
import type {PlatformName} from '../types/platform';

interface SearchState {
  query: string;
  selectedPlatforms: PlatformName[];
  setQuery: (q: string) => void;
  togglePlatform: (platform: PlatformName) => void;
}

export const useSearchStore = create<SearchState>(set => ({
  query: '',
  selectedPlatforms: ['blinkit', 'zepto'],
  setQuery: (q) => set({query: q}),
  togglePlatform: (platform) =>
    set(state => {
      const platforms = state.selectedPlatforms.includes(platform)
        ? state.selectedPlatforms.filter(p => p !== platform)
        : [...state.selectedPlatforms, platform];
      return {selectedPlatforms: platforms.length > 0 ? platforms : state.selectedPlatforms};
    }),
}));
