import { gql, useQuery } from '@apollo/client';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

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

function MovieList() {
  const { loading, error, data } = useQuery(GET_MOVIES);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error : {error.message}</p>;

  return data.movies.map(({ title, year, imgUrl, avgRating }) => (
    <Grid item xs={4}>
      <Card sx={{ maxWidth: 270 }}>
        <CardActionArea>
          <CardMedia
            component="img"
            image={`${imgUrl}`}
            width="270"
            height="400"
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
    <div>
      <Typography variant="h3" component="div">
        Shitty Movies
      </Typography>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={2}>
          <MovieList />
        </Grid>
      </Box>
    </div>
  );
}
