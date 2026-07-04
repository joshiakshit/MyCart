import React from 'react';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import {useAccounts} from '../hooks/useAccounts';
import {PlatformBadge} from '../components/PlatformBadge';
import type {PlatformName} from '../types/platform';

const PLATFORMS: {name: PlatformName; label: string}[] = [
  {name: 'blinkit', label: 'Blinkit'},
  {name: 'zepto', label: 'Zepto'},
];

export function AccountsScreen() {
  const {data: accounts, isLoading} = useAccounts();

  const isLinked = (platform: PlatformName) =>
    accounts?.some(a => a.platform === platform && a.is_active) ?? false;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Linked Accounts</Text>
      <Text style={styles.subtitle}>
        Link your accounts to compare personalized prices.
      </Text>

      <View style={styles.list}>
        {PLATFORMS.map(p => (
          <View key={p.name} style={styles.accountRow}>
            <PlatformBadge platform={p.name} />
            <Text style={styles.accountLabel}>{p.label}</Text>
            <TouchableOpacity
              style={[
                styles.linkButton,
                isLinked(p.name) && styles.linkedButton,
              ]}>
              <Text
                style={[
                  styles.linkText,
                  isLinked(p.name) && styles.linkedText,
                ]}>
                {isLinked(p.name) ? 'Linked' : 'Link Account'}
              </Text>
            </TouchableOpacity>
          </View>
        ))}
      </View>
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
    marginBottom: 24,
  },
  list: {
    gap: 12,
  },
  accountRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 1},
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  accountLabel: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginLeft: 12,
  },
  linkButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    backgroundColor: '#2E7D32',
  },
  linkedButton: {
    backgroundColor: '#E8F5E9',
  },
  linkText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 13,
  },
  linkedText: {
    color: '#2E7D32',
  },
});
