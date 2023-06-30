"use client";

import { useState } from 'react';
import HPOSelect from './components/HPOSelect';
import Header from './components/Header';
import Footer from './components/Footer';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Fab from '@mui/material/Fab';
import SendIcon from '@mui/icons-material/Send';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { Disorder, HPO, getRareDisorders } from './api/service';

export default function Home() {
  const [ currentHPOs, setCurrentHPOs ] = useState<HPO[]>([]);
  const [ disorders, setDisorders ] = useState<Disorder[]>([]);

  const handleGetDisorders = async () => {
    try {
      const disorders = await getRareDisorders(currentHPOs.map(item => item.id));
      setDisorders(disorders);
    } catch(err) {
    }
  }

  function renderDisorderRow(props: ListChildComponentProps) {
    const { index, style } = props;
    const { id, orpha_code, name, expert_link, freq } = disorders[index]

    const handleClick = () => {
      window.open(expert_link, "_blank", "noreferrer");
    }
  
    return (
      <ListItem style={style} key={index} component="div" disablePadding>
        <ListItemButton onClick={handleClick}>
          <ListItemText primary={name} secondary={`freq: ${(freq * 100).toFixed(2)}%`}/>
        </ListItemButton>
      </ListItem>
    );
  }
  
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-12">
      <Header />

      <div className="relative w-full flex-1 pt-10 pb-10 lg:flex max-w-5xl">
        <div className="flex-1 pr-10">
          <p className="text-zinc-700 text-sm leading-8">We accepts a list of symptoms (HPO IDs) as input and returns an ordered list of the most relevant rare conditions. The method by which relevant conditions are selected is up to your discretion.</p>
          <br/><br/>
          <HPOSelect value={currentHPOs} onChange={(value) => setCurrentHPOs(value)}/>
          <br/><br/>
          <Fab variant="extended" onClick={handleGetDisorders}>
            <SendIcon sx={{ mr: 1 }} />
            Get Disorder List
          </Fab>
        </div>
        <div className="flex-1 pl-10">
        <Box
          sx={{ width: '100%', bgcolor: 'background.paper' }}
        >
          <FixedSizeList
            height={350}
            itemSize={90}
            itemCount={disorders.length}
            overscanCount={5}
          >
            {renderDisorderRow}
          </FixedSizeList>
        </Box>
        <p className="text-xs	text-zinc-700 mt-3">* Click any of the above item to see orpha data</p>
        </div>
      </div>

      <Footer />
    </main>
  )
}
