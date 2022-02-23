import {useEffect, useState} from "react";

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Container from '@mui/material/Container';
import LinkIcon from '@mui/icons-material/Link';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

import { createTheme, ThemeProvider } from '@mui/material/styles';


const theme = createTheme({
  palette: {
    background: {
      default: "#e4f0e2"
    }
  }
});


const MediaCard = ({title, desc, origen, setDatasetId, itemId}) => {
  
  const handleClick = (itemId) => {
    setDatasetId(itemId)
  }

  return (
    <Card sx={{ maxWidth: 500 }}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {title}
        </Typography>
        <Chip label={origen} />
        <Typography variant="body2" color="text.secondary">
          {desc}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={(() => handleClick(itemId))}> Visita </Button>
      </CardActions>
    </Card>
  );
}


function FeaturedPost({dataset}) {

  return (
        <Card sx={{ display: 'flex' }}>
          <CardContent sx={{ flex: 1}}>
            <Typography component={'div'}>
              <h1> {dataset.title}</h1>
            </Typography>
            <Chip label={dataset.origen} />
            <Chip label={dataset.category} />
            <Typography variant="subtitle1" color="text.secondary">
              12/10/2020
            </Typography>
            <Typography variant="subtitle1" paragraph>
              {dataset.description}
            </Typography>
            <Button variant="contained" 
              startIcon={<LinkIcon />}
              href={dataset.web_url}
              target="_blank"
            > 
              Link 
            </Button>
          </CardContent>
        </Card>
  );
}


const SelectedDataset = ({catalog, datasetId, dataset, setDatasetId}) => {
  const [recomended, setRecomended] = useState([])
  // Number of datasets to show as recommended
  const numRecomended = 5

  const fetchRecomended = async () => {
    try {
      const response = await fetch(`http://localhost:8000/similar/${datasetId}` , {mode:'cors'})
      const similarList = await response.json()
      setRecomended(similarList.message.slice(0, numRecomended))
    } catch(error) {
      console.log(error)
    }
  }
  
  useEffect(() => {
    fetchRecomended()
  }, [])

  return(
    <div>
      <Box sx={{ p: 2, border: '1px dashed grey' }}>
        <Button variant="contained" 
          startIcon={<ArrowBackIcon />}
          onClick={() => setDatasetId("")}
        > 
          Torna 
        </Button>
      </Box>
      <FeaturedPost dataset={dataset}/>
      <Box sx={{ p: 5, border: '1px dashed grey' }}></Box>
      <h2> Datasets similars </h2>
      <Stack spacing={2}>
        {
          recomended.map((recomendedId, index) => {
            if(datasetId !== recomendedId){
              const recomendedDataset = catalog[recomendedId]
              return(
                <MediaCard key={index} 
                  title={recomendedDataset.title} 
                  desc={recomendedDataset.description} 
                  origen={recomendedDataset.origen} 
                  setDatasetId={setDatasetId}
                  itemId={recomendedId}
                />
              )
            }
          }
        )
        }
      </Stack>
    </div>
  )
}

function App() {

  const [catalog, setCatalog] = useState([])
  const [datasetId, setDatasetId] = useState("")

  const fetchCatalog = async () => {
    try {
      const response = await fetch("http://localhost:8000/catalog")
      const retrievedCatalog = await response.json()
      setCatalog(retrievedCatalog.message)
    } catch(error) {
      console.log(error)
    }
  }

  useEffect(() => {
    fetchCatalog();
    }, []);

  return (
    <>
      <ThemeProvider theme={theme}>   
      <CssBaseline />   
        <main>
          <Box sx={{ pt: 8, pb: 6 }} > 
            <Container maxWidth="sm">
              {datasetId !== "" ? (
                <SelectedDataset 
                  catalog={catalog} 
                  datasetId={datasetId} 
                  dataset={catalog[datasetId]}
                  setDatasetId={setDatasetId}
                />
              )
              :
              (
                <Stack spacing={2}>
                  {catalog.map((dataset, index) => (
                    <MediaCard key={index} 
                      title={dataset.title} 
                      desc={dataset.description} 
                      origen={dataset.origen} 
                      setDatasetId={setDatasetId}
                      itemId={index}
                    />
                  ))}
                </Stack>            
              )}
            </Container>
          </Box>
        </main>    
      </ThemeProvider>
    </>
  );
}

export default App;
