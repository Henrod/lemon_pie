import { Grid, Button, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    textAlign: "center",
    flexGrow: 1,
    margin: theme.spacing(2),
  },
  gridContainer: {
    spacing: 4,
    direction: "row",
    justify: "center",
  },
  button: {
    fontSize: "63px",
  },
}));

const VotesBox = ({ user, vote, handleClick, validEmojis }) => {
  const classes = useStyles();
  const getColor = (key) => (key === vote ? "primary" : "default");
  const getVariant = (key) => (key === vote ? "contained" : "text");

  return (
    <Paper key={user.key} className={classes.paper}>
      <Typography variant="h4">{user.name}</Typography>
      <Grid container key={user.key} className={classes.gridContainer}>
        {validEmojis.map(({ key, value }) => (
          <Grid key={key} item lg={3} md={4} sm={6} xs={12}>
            <Button
              key={key}
              className={classes.button}
              onClick={() => handleClick(key, user.key)}
              color={getColor(key)}
              variant={getVariant(key)}
              fullWidth
            >
              {`${value}`}
            </Button>
          </Grid>
        ))}
      </Grid>
      <Typography variant="h4">{vote}</Typography>
    </Paper>
  );
};

export default VotesBox;
