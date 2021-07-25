import React, { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Client from "../api/client";
import { Grid, ThemeProvider, createMuiTheme } from "@material-ui/core";
import { VotesBox, TopBar, LinkButton } from "../components";
import { redirectComponent, loginState } from "../api/login";

const useStyles = makeStyles((theme) => ({
  gridContainer: {
    spacing: 4,
    direction: "column",
  },
  gridItem: {
    marginTop: theme.spacing(4),
  },
}));

const theme = createMuiTheme({});

const Vote = () => {
  const classes = useStyles();

  const [state, setState] = useState({
    isLogged: true,
    votes: {},
    users: {},
    user: {},
    validEmojis: [],
    canVote: false,
  });

  useEffect(() => {
    const client = new Client();
    const getVotes = async () => {
      try {
        const me = await client.getMe();
        const user_key = me.data.key;

        const votes = await client.getUserVotes(user_key);

        const votesState = {};
        const usersState = {};
        for (let [user, data] of Object.entries(votes.data.votes)) {
          votesState[user] = "___";
          usersState[user] = data.user;
          for (let [key, { count }] of Object.entries(data.votes)) {
            if (count > 0) {
              votesState[user] = key;
            }
          }
        }

        const validEmojis = (await client.getValidEmojis()).data["emojis"];

        setState((state) => ({
          ...state,
          user: { key: user_key },
          votes: votesState,
          users: usersState,
          validEmojis: validEmojis,
          canVote: votes.data.can_vote,
        }));
      } catch (error) {
        console.log("failed to fetch from api", error);
        setState((state) => loginState(error, state));
      }
    };

    getVotes();
  }, [state.user.key]);

  const handleClick = (vote, dst) => {
    const client = new Client();
    const setVote = async () => await client.setVote(vote, dst);
    const prevVote = state.votes[dst];
    try {
      setState({
        ...state,
        votes: { ...state.votes, [dst]: vote },
        users: { ...state.users },
      });
      setVote();
    } catch (error) {
      setState(
        loginState(error, {
          votes: { ...state.votes, [dst]: prevVote },
          users: { ...state.users },
        })
      );
      console.log("failed to set on api", error);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <TopBar />
      <LinkButton to="/" text="Home" canVote={state.canVote}></LinkButton>
      {redirectComponent(state)}
      <Grid container className={classes.gridContainer}>
        {Object.keys(state.votes)
          .sort()
          .map((user) => (
            <Grid
              item
              key={user}
              lg={3}
              md={12}
              sm={12}
              xs={12}
              className={classes.gridItem}
            >
              <VotesBox
                key={user}
                user={state.users[user]}
                vote={state.votes[user]}
                handleClick={handleClick}
                validEmojis={state.validEmojis}
                canVote={state.canVote}
              />
            </Grid>
          ))}
      </Grid>
    </ThemeProvider>
  );
};

export default Vote;
