import { parseSnapshot } from "@carlo/core";
import fixture from "@carlo/core/snapshot.fixture.json";
import { FlatList, StyleSheet, Text, View } from "react-native";

// Phase 1 wiring check: decode the shared snapshot fixture through
// @carlo/core. The live snapshot download replaces this in a later change.
const snapshot = parseSnapshot(JSON.stringify(fixture));

export default function ExploreScreen() {
  return (
    <FlatList
      data={snapshot.churches}
      keyExtractor={(church) => church.slug}
      ListHeaderComponent={
        <Text style={styles.header}>
          {snapshot.churches.length} churches, {snapshot.events.length} events
        </Text>
      }
      renderItem={({ item }) => (
        <View style={styles.row}>
          <Text style={styles.name}>{item.name}</Text>
          <Text style={styles.city}>
            {item.city}, {item.state}
          </Text>
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  header: { padding: 16, fontSize: 14, color: "#555" },
  row: { paddingHorizontal: 16, paddingVertical: 12 },
  name: { fontSize: 17 },
  city: { fontSize: 14, color: "#555" },
});
