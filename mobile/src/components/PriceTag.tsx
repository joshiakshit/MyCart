import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

interface PriceTagProps {
  price: number;
  mrp: number | null;
  isBestPrice?: boolean;
}

export function PriceTag({price, mrp, isBestPrice = false}: PriceTagProps) {
  const hasDiscount = mrp !== null && mrp > price;

  return (
    <View style={styles.container}>
      <Text style={[styles.price, isBestPrice && styles.bestPrice]}>
        ₹{price}
      </Text>
      {hasDiscount && <Text style={styles.mrp}>₹{mrp}</Text>}
      {isBestPrice && <Text style={styles.bestLabel}>BEST</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  price: {
    fontSize: 18,
    fontWeight: '700',
    color: '#333',
  },
  bestPrice: {
    color: '#2E7D32',
  },
  mrp: {
    fontSize: 14,
    color: '#999',
    textDecorationLine: 'line-through',
  },
  bestLabel: {
    fontSize: 10,
    fontWeight: '800',
    color: '#fff',
    backgroundColor: '#2E7D32',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
    overflow: 'hidden',
  },
});
