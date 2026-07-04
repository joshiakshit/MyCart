export type PlatformName = 'blinkit' | 'zepto';

export interface LinkedAccount {
  platform: PlatformName;
  platform_user_id: string | null;
  is_active: boolean;
  delivery_address_id: string | null;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
