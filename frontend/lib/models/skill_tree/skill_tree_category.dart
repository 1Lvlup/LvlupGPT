enum SkillTreeCategory {
  general,
  coding,
  data,
  scrapeSynthesize,
}

extension SkillTreeTypeExtension on SkillTreeCategory {
  Map<SkillTreeCategory, String> _stringValues = {
    SkillTreeCategory.general: 'General',
    SkillTreeCategory.coding: 'Coding',
    SkillTreeCategory.data: 'Data',
    SkillTreeCategory.scrapeSynthesize: 'Scrape/Synthesize',
  };

  Map<SkillTreeCategory, String> _jsonFileNames = {
    SkillTreeCategory.general: 'general_tree_structure.json',
    SkillTreeCategory.coding: 'coding_tree_structure.json',
    SkillTreeCategory.data: 'data_tree_structure.json',
    SkillTreeCategory.scrapeSynthesize: 'scrape_synthesize_tree_structure.json',
  };

  String get stringValue => _stringValues[this] ?? '';

  String get jsonFileName => _jsonFileNames[this] ?? '';
}
