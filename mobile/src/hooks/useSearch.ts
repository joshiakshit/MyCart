import {useQuery} from '@tanstack/react-query';
import {searchApi} from '../api/endpoints';
import type {SearchResponse} from '../types/product';

export function useSearch(query: string, platforms: string[]) {
  return useQuery<SearchResponse>({
    queryKey: ['search', query, platforms],
    queryFn: async () => {
      const response = await searchApi.search(query, platforms);
      return response.data;
    },
    enabled: query.length >= 2,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
