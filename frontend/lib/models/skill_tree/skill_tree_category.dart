// Define an enum `SkillTreeCategory` with four categories: general, coding, data, and scrapeSynthesize.
enum SkillTreeCategory { general, coding, data, scrapeSynthesize }

// Extension of the `SkillTreeCategory` enum, providing additional functionality.
extension SkillTreeTypeExtension on SkillTreeCategory {
  // A map that maps each category to its string representation.
  Map<SkillTreeCategory, String> _stringValues = {
    SkillTreeCategory.general: 'General',
    SkillTreeCategory.coding: 'Coding',
    SkillTreeCategory.data: 'Data',
    SkillTreeCategory.scrapeSynthesize: 'Scrape/Synthesize',
  };

  // A map that maps each category to the name of its corresponding JSON file.
  Map<SkillTreeCategory, String> _jsonFileNames = {
    SkillTreeCategory.general: 'general_tree_structure.json',
    SkillTreeCategory.coding: 'coding_tree_structure.json',
    SkillTreeCategory.data: 'data_tree_structure.json',
    SkillTreeCategory.scrapeSynthesize: 'scrape_synthesize
