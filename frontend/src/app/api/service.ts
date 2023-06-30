import { myAxios } from './myAxios';

export type HPO = {
    id: number,
    legal_id: string,
    name: string,
}
export type Disorder = {
    id: number,
    orpha_code: number,
    name: string,
    expert_link: string,
    freq: number
}

export const getHPOs = async () => {
    const { data } = await myAxios.get('/hpo')
    return data as HPO[]
}

export const getRareDisorders = async (hpoIds: number[]) => {
    const { data } = await myAxios.get(`/rare_conditions?hpos=${hpoIds.map(item => item.toString()).join(',')}`)
    return data as Disorder[]
}