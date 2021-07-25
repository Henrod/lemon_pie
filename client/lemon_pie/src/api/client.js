const axios = require("axios");

class Client {
  constructor(url) {
    this.url = process.env.REACT_APP_API_URL || "https://localhost:5000";
    this.instance = axios.create({
      withCredentials: true,
      baseURL: `${this.url}/api`,
    });
  }

  async getVotes() {
    return await this.instance.get("votes");
  }

  async getUserVotes(user) {
    return await this.instance.get(`users/${user}/votes`);
  }

  async getValidEmojis() {
    return await this.instance.get(`/emojis`);
  }

  async setVote(vote, dst) {
    return await this.instance.put("votes", {
      dst: { key: dst },
      key: vote,
    });
  }

  async login(token) {
    return await this.instance.post("login/callback", null, {
      headers: {
        Authorization: token,
      },
    });
  }

  async getMe() {
    return await this.instance.get("me");
  }
}

export default Client;
