import { Grid, Paper, Typography, Box } from "@material-ui/core";
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
  gridItem: {
    fontSize: "63px",
  },
}));

const SummaryBox = ({ user, votes }) => {
  const classes = useStyles();

  return (
    <Paper key={user.key} className={classes.paper}>
      <Typography variant="h4">{user.name}</Typography>
      <Grid container key={user.key} className={classes.gridContainer}>
        {Object.keys(votes).map((emojiKey) => (
          <Grid key={emojiKey} item lg={3} md={4} sm={6} xs={12}>
            <Box className={classes.gridItem}>
              {`${votes[emojiKey]["value"]} ${votes[emojiKey]["count"]}`}
            </Box>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default SummaryBox;
