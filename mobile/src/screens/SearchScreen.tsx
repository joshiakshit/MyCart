import React, {useState} from 'react';
import {ActivityIndicator, FlatList, StyleSheet, Text, View} from 'react-native';
import {SearchBar} from '../components/SearchBar';
import {ProductCard} from '../components/ProductCard';
import {useSearch} from '../hooks/useSearch';
import {useSearchStore} from '../stores/useSearchStore';

export function SearchScreen() {
  const [inputValue, setInputValue] = useState('');
  const {query, selectedPlatforms, setQuery} = useSearchStore();
  const {data, isLoading, error} = useSearch(query, selectedPlatforms);

  const handleSubmit = () => {
    setQuery(inputValue.trim());
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>MyCart</Text>
      <SearchBar
        value={inputValue}
        onChangeText={setInputValue}
        onSubmit={handleSubmit}
      />

      {isLoading && (
        <ActivityIndicator size="large" style={styles.loader} color="#2E7D32" />
      )}

      {error && (
        <Text style={styles.error}>
          Something went wrong. Please try again.
        </Text>
      )}

      {data && data.results.length === 0 && (
        <Text style={styles.empty}>No results found for "{query}"</Text>
      )}

      <FlatList
        data={data?.results ?? []}
        keyExtractor={(item, index) => `${item.name}-${index}`}
        renderItem={({item}) => <ProductCard product={item} />}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafafa',
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: '#2E7D32',
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  loader: {
    marginTop: 32,
  },
  error: {
    textAlign: 'center',
    color: '#D32F2F',
    marginTop: 32,
    fontSize: 14,
  },
  empty: {
    textAlign: 'center',
    color: '#999',
    marginTop: 32,
    fontSize: 14,
  },
  list: {
    paddingVertical: 8,
  },
});
