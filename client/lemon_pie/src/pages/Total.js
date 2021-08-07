import React, { useEffect, useState } from "react";
import Client from "../api/client";
import { makeStyles } from "@material-ui/core/styles";
import { TopBar, SummaryBox, LinkButton } from "../components";
import {
  ThemeProvider,
  createMuiTheme,
  Grid,
  Typography,
  Box,
} from "@material-ui/core";
import { redirectComponent, loginState } from "../api/login";
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
}));

const Summary = () => {
  const classes = useStyles();
  const [state, setState] = useState({
    votes: {},
    users: {},
    startDate: null,
    endDate: null,
    isLogged: true,
  });

  useEffect(() => {
    const client = new Client();
    const getVotes = async () => {
      try {
        const votes = await client.getTotalVotes();

        const votesState = {};
        const usersState = {};
        for (let [user, data] of Object.entries(votes.data.total.votes)) {
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
          startDate: votes.data.total.start_date,
          endDate: votes.data.total.end_date,
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
        <LinkButton to="/" text={translatedText("Total.summary")} />
        <Typography variant="h4">
          {state.startDate} - {state.endDate}
        </Typography>
      </Box>
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
