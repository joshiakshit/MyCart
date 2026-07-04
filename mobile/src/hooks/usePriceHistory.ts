import {useQuery} from '@tanstack/react-query';
import {pricesApi} from '../api/endpoints';

export function usePriceHistory(
  platform: string,
  productId: string,
  days: number = 30,
) {
  return useQuery({
    queryKey: ['priceHistory', platform, productId, days],
    queryFn: async () => {
      const response = await pricesApi.history(platform, productId, days);
      return response.data;
    },
    enabled: !!platform && !!productId,
  });
}
