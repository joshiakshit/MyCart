import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {SearchScreen} from '../screens/SearchScreen';
import {CompareScreen} from '../screens/CompareScreen';
import {AccountsScreen} from '../screens/AccountsScreen';
import {SettingsScreen} from '../screens/SettingsScreen';

const Tab = createBottomTabNavigator();

export function AppNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#2E7D32',
        tabBarInactiveTintColor: '#999',
        tabBarStyle: {
          backgroundColor: '#fff',
          borderTopWidth: 0,
          elevation: 8,
          shadowColor: '#000',
          shadowOffset: {width: 0, height: -2},
          shadowOpacity: 0.1,
          shadowRadius: 4,
        },
      }}>
      <Tab.Screen
        name="Search"
        component={SearchScreen}
        options={{tabBarLabel: 'Search'}}
      />
      <Tab.Screen
        name="Compare"
        component={CompareScreen}
        options={{tabBarLabel: 'Compare'}}
      />
      <Tab.Screen
        name="Accounts"
        component={AccountsScreen}
        options={{tabBarLabel: 'Accounts'}}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{tabBarLabel: 'Settings'}}
      />
    </Tab.Navigator>
  );
}
