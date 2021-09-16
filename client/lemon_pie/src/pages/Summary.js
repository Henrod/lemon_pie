import {
  Box,
  createMuiTheme,
  Grid,
  ThemeProvider,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React, { useEffect, useState } from "react";
import Client from "../api/client";
import { loginState, redirectComponent } from "../api/login";
import { LinkButton, SummaryBox, TopBar } from "../components";
import { translatedText } from "../translation";

const theme = createMuiTheme({});

const useStyles = makeStyles((theme) => ({
  gridContainer: {
    spacing: 4,
    direction: "column",
  },
  gridItem: {
    marginTop: theme.spacing(4),
  },
  text: {
    marginTop: theme.spacing(4),
  },
}));

const Summary = () => {
  const classes = useStyles();
  const [state, setState] = useState({
    votes: {},
    users: {},
    isLogged: true,
    canVote: false,
    isTotalEnabled: false,
    voteStartsAt: null,
    voteEndsAt: null,
    voteDate: null,
  });

  useEffect(() => {
    const client = new Client();
    const getVotes = async () => {
      try {
        const votes = await client.getVotes();
        const total = await client.getIsTotalEnabled();

        const votesState = {};
        const usersState = {};
        for (let [user, data] of Object.entries(votes.data.votes)) {
          votesState[user] = {};
          usersState[user] = data.user;
          for (let [key, count] of Object.entries(data.votes)) {
            votesState[user][key] = count;
          }
        }

        setState((state) => ({
          ...state,
          votes: votesState,
          users: usersState,
          canVote: votes.data.can_vote,
          isTotalEnabled: total.data.is_enabled,
          voteStartsAt: votes.data.times.starts_at,
          voteEndsAt: votes.data.times.ends_at,
          voteDate: votes.data.end_date,
        }));
      } catch (error) {
        console.log("failed to fetch from api", error);
        setState((state) => loginState(error, state));
      }
    };

    getVotes();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <TopBar />
      {redirectComponent(state)}
      <Box display="flex" alignItems="center">
        <LinkButton
          to="/votes"
          text={translatedText("Summary.vote")}
          disabled={!state.canVote}
        />
        <LinkButton
          to="/total"
          text={translatedText("Summary.total")}
          disabled={!state.isTotalEnabled}
        />
        {state.voteEndsAt && (
          <Typography variant="h5">
            {translatedText("Summary.voteEndsAt")} {state.voteEndsAt}
          </Typography>
        )}
        {state.voteStartsAt && (
          <Typography variant="h5">
            {translatedText("Summary.voteStartsAt")} {state.voteStartsAt}
          </Typography>
        )}
      </Box>
      {state.voteDate && (
        <Typography className={classes.text} align="center" variant="h5">
          {state.voteDate}
        </Typography>
      )}
      <Grid container className={classes.gridContainer}>
        {Object.keys(state.votes).map((user) => (
          <Grid
            item
            key={user}
            lg={3}
            md={12}
            sm={12}
            xs={12}
            className={classes.gridItem}
          >
            <SummaryBox
              key={user}
              user={state.users[user]}
              votes={state.votes[user]}
            />
          </Grid>
        ))}
      </Grid>
    </ThemeProvider>
  );
};

export default Summary;
