import { useParams } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Typography } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';


const GET_MOVIE = gql`
  query GetMovie($movieId: Int!) {
    movie(movieId: $movieId) {
      title
      year
      imgUrl
      description
    }
  }
`;

const GET_REVIEWS = gql`
  query GetReviews($movieId: Int!) {
    reviews(movieId: $movieId) {
      username
      rating
      text
    }
  }
`;

export default function MovieDetail() {
    let { movieId } = useParams();
    movieId = parseInt(movieId);
    
    const movieResult = useQuery(GET_MOVIE, {
        variables: { movieId },
    });
    const reviewsResult = useQuery(GET_REVIEWS, {
        variables: { movieId },
    });
  
    if (movieResult.loading || reviewsResult.loading) return <p>Loading...</p>;
    if (movieResult.error || reviewsResult.error) return <p>Error : {movieResult.error.message || reviewsResult.error.message}</p>;

    const { title, year, imgUrl, description } = movieResult.data.movie;
    const reviews = reviewsResult.data.reviews.map(({ username, rating, text }) => (
        <Card>
            <CardContent>
                <Typography variant="h6">
                    {username} - {rating} / 10
                </Typography>
                <Typography>
                    {text}
                </Typography>
            </CardContent>
        </Card>
    ));

    return (
        <Grid container spacing={2}>
            <Grid item xs={3}>
                <Card>
                    <CardMedia
                        component="img"
                        image={`${imgUrl}`}
                        alt={`${title} Poster`}
                    />
                </Card>
            </Grid>
            <Grid item xs={9}>
                <Card>
                    <CardContent>
                        <Typography variant="h5" component="div">
                            {title}
                        </Typography>
                        <Typography variant="subtitle1">
                            ({year})
                        </Typography>
                        <Typography>
                            {description}
                        </Typography>
                    </CardContent>
                </Card>
                {reviews}
            </Grid>
        </Grid>
    )
}