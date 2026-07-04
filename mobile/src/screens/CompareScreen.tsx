import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

export function CompareScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Compare</Text>
      <Text style={styles.subtitle}>
        Select a product from search results to compare prices across platforms.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafafa',
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: '#333',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
  },
});
