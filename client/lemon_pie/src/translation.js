const texts = {
  "Vote.missing": {
    "pt-br": "Seus votos só serão contados após votar em todos",
    en: "Your votes will only count after voting for all",
  },
};

const defaultLanguage = "pt-br";

const translatedText = (text, language = defaultLanguage) =>
  (texts[text] || {})[language] || "";

export { translatedText };
