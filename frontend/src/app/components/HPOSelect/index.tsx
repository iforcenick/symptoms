"use client";

import React, { useEffect, useState } from 'react'
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { getHPOs } from '../../api/service';
import type { HPO } from '../../api/service';

type HPOSelectProps = {
    onChange: (value: HPO[]) => void;
    value: HPO[];
}

const HPOSelect: React.FC<HPOSelectProps> = ({onChange, value}) => {
    const [ hpos, setHPOs ] = useState<HPO[]>([]);
    const handleChange = (event: React.SyntheticEvent, value: HPO[]) => {
        onChange(value)
    }
    useEffect(() => {
        (async() => {
            try {
                const data = await getHPOs()
                setHPOs(data)
                console.log(data.length)
                onChange([data[0]])
            } catch(err) {
                setHPOs([])
            }
        })()
    }, [])
    return (
        <Autocomplete
            multiple
            id="tags-outlined"
            options={hpos}
            getOptionLabel={(option) => option.name}
            value={value}
            onChange={handleChange}
            filterSelectedOptions
            renderInput={(params) => (
              <TextField
                {...params}
                label="Selected HPOs"
                placeholder="Add new HPO"
              />
            )}
        />
    )
}

export default HPOSelect;