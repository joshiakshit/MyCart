import {useQuery, useMutation, useQueryClient} from '@tanstack/react-query';
import {accountsApi} from '../api/endpoints';

export function useAccounts() {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: async () => {
      const response = await accountsApi.list();
      return response.data.accounts;
    },
  });
}

export function useLinkAccount() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      platform,
      phoneNumber,
      otp,
    }: {
      platform: string;
      phoneNumber: string;
      otp: string;
    }) => accountsApi.verifyLink(platform, phoneNumber, otp),
    onSuccess: () => {
      queryClient.invalidateQueries({queryKey: ['accounts']});
    },
  });
}
