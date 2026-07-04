import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import type {PlatformName} from '../types/platform';

const PLATFORM_COLORS: Record<PlatformName, string> = {
  blinkit: '#F9CB28',
  zepto: '#7B2D8E',
};

const PLATFORM_LABELS: Record<PlatformName, string> = {
  blinkit: 'Blinkit',
  zepto: 'Zepto',
};

interface PlatformBadgeProps {
  platform: PlatformName;
}

export function PlatformBadge({platform}: PlatformBadgeProps) {
  return (
    <View
      style={[styles.badge, {backgroundColor: PLATFORM_COLORS[platform] ?? '#666'}]}>
      <Text style={styles.text}>{PLATFORM_LABELS[platform] ?? platform}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    alignSelf: 'flex-start',
  },
  text: {
    color: '#fff',
    fontSize: 11,
    fontWeight: '700',
  },
});
