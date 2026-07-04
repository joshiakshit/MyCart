export interface PlatformPrice {
  platform: string;
  price: number;
  mrp: number | null;
  discount_pct: number | null;
  in_stock: boolean;
  delivery_eta_minutes: number | null;
  platform_product_id: string;
}

export interface ComparedProduct {
  name: string;
  brand: string | null;
  unit_quantity: string | null;
  image_url: string | null;
  prices: PlatformPrice[];
  best_price: PlatformPrice | null;
}

export interface PlatformStatus {
  status: string;
  response_time_ms: number | null;
  message: string | null;
}

export interface SearchResponse {
  query: string;
  results: ComparedProduct[];
  platform_status: Record<string, PlatformStatus>;
}

export interface PriceHistoryPoint {
  price: number;
  mrp: number | null;
  in_stock: boolean;
  captured_at: string;
}
