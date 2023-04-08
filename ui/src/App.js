import { gql, useQuery } from '@apollo/client';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const GET_MOVIES = gql`
  query GetMovies {
    movies {
      id
      title
      year
      imgUrl
      avgRating
    }
  }
`;

function NavBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h5" component="div" sx={{ flexGrow: 1 }}>
            Shitty Movies
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

function MovieList() {
  const { loading, error, data } = useQuery(GET_MOVIES);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error : {error.message}</p>;

  return data.movies.map(({ title, year, imgUrl, avgRating }) => (
    <Grid item xs={3}>
      <Card sx={{ maxWidth: 270 }}>
        <CardActionArea>
          <CardMedia
            component="img"
            image={`${imgUrl}`}
            alt={`${title} Poster`}
          />
          <CardContent>
            <Typography variant="h5" component="div">
              {title}
            </Typography>
            <Typography variant="subtitle1">
              ({year})
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              {avgRating}/10
            </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
    </Grid>
  ));
}

export default function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <NavBar />
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={2}>
          <MovieList />
        </Grid>
      </Box>
    </ThemeProvider>
  );
}
