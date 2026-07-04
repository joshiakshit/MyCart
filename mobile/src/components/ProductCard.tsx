import React from 'react';
import {Image, StyleSheet, Text, View} from 'react-native';
import type {ComparedProduct} from '../types/product';
import type {PlatformName} from '../types/platform';
import {PlatformBadge} from './PlatformBadge';
import {PriceTag} from './PriceTag';

interface ProductCardProps {
  product: ComparedProduct;
}

export function ProductCard({product}: ProductCardProps) {
  return (
    <View style={styles.card}>
      <View style={styles.header}>
        {product.image_url && (
          <Image source={{uri: product.image_url}} style={styles.image} />
        )}
        <View style={styles.info}>
          <Text style={styles.name} numberOfLines={2}>
            {product.name}
          </Text>
          {product.brand && (
            <Text style={styles.brand}>{product.brand}</Text>
          )}
          {product.unit_quantity && (
            <Text style={styles.unit}>{product.unit_quantity}</Text>
          )}
        </View>
      </View>

      <View style={styles.prices}>
        {product.prices.map(p => (
          <View key={p.platform} style={styles.priceRow}>
            <PlatformBadge platform={p.platform as PlatformName} />
            <PriceTag
              price={p.price}
              mrp={p.mrp}
              isBestPrice={product.best_price?.platform === p.platform}
            />
            {!p.in_stock && <Text style={styles.outOfStock}>Out of stock</Text>}
            {p.in_stock && p.delivery_eta_minutes && (
              <Text style={styles.eta}>{p.delivery_eta_minutes} min</Text>
            )}
          </View>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 6,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 1},
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  header: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  image: {
    width: 64,
    height: 64,
    borderRadius: 8,
    marginRight: 12,
  },
  info: {
    flex: 1,
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  brand: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  unit: {
    fontSize: 12,
    color: '#999',
    marginTop: 2,
  },
  prices: {
    gap: 8,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  outOfStock: {
    fontSize: 12,
    color: '#D32F2F',
    fontWeight: '600',
  },
  eta: {
    fontSize: 12,
    color: '#666',
    marginLeft: 'auto',
  },
});
