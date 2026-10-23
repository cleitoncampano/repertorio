import {useQuery} from '@tanstack/react-query';
import {api} from './api';
import type {Skill} from './skillCatalog';
import type {Repo} from './repoCatalog';

// personal: catálogo escolhido pelo usuário; senão, sugestões do pacote.
export type Catalog={skills:Skill[];repos:Repo[];personal:boolean};
export const useCatalog=()=>useQuery({queryKey:['catalog'],queryFn:()=>api<Catalog>('/catalog'),staleTime:Infinity});
