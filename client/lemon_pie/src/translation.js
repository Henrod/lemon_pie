const texts = {
  "Vote.missing": {
    "pt-br": "Seus votos só serão contados após votar em todos",
    en: "Your votes will only count after voting for all",
  },
  "Vote.summary": {
    "pt-br": "Home",
    en: "Home",
  },
  "Summary.vote": {
    "pt-br": "Votar",
    en: "Vote",
  },
  "Summary.total": {
    "pt-br": "Total",
    en: "Total",
  },
  "Summary.voteStartsAt": {
    "pt-br": "Votação começa às",
    en: "Vote starts at",
  },
  "Summary.voteEndsAt": {
    "pt-br": "Votação termina às",
    en: "Vote ends at",
  },
  "Total.summary": {
    "pt-br": "Home",
    en: "Home",
  },
};

const defaultLanguage = process.env.REACT_APP_LANGUAGE || "en";

const translatedText = (text, language = defaultLanguage) =>
  (texts[text] || {})[language] || "";

export { translatedText };
