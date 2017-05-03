from __future__ import unicode_literals

import re
import csv
import tweepy
import ast

from datetime import datetime

from tweepy.error import TweepError

from unicodedata import normalize
from TwitterSearch import TwitterSearchOrder, TwitterSearch, TwitterSearchException

from .models import Tweet


def get_tweets():
    #run: ./manage.py shell -c="from tweets.utils import get_tweets; get_tweets()"

    #keywords = ["arrombada", "arrombado", "asno", "acefalo","babaca", "babuino", "baitola", "biba", "bicha", "bixa", "bixinha", "bobo", "boceta", "boquete", "borra", "bosta", "buceta", "boceta", "bundao", "burro", "cacete", "cadela", "cagar", "cala", "cale", "caralho", "caralio", "chupe", "come", "corno", "cu", "cusao", "cuzao", "desgracado", "disgracado", "egua", "enraba", "fdp", "fiderapariga", "fidumaegua", "filhodaputa", "filhodeumaputa", "foda", "fodase", "foder", "fuder", "fudeu", "fudido", "gay", "grelo", "idiota", "inferno", "jegue", "louco", "macaco", "mamar", "marica", "merda", "mijao", "otario", "pariu", "pau", "peidar", "pica", "pinto", "piriguete", "piroca", "piru", "porra", "puta", "quinto", "rapariga", "retardado", "rola", "siririca", "tesuda", "tomar", "vagabundo", "vaite", "veado", "velha", "viado", "xereca"]
    #keywords = ['foda se', 'foda-se', 'vai te foder', 'vai se foder', 'vai te fuder', 'vai se foder', 'vai tomar no cú', 'vai tomar no cu', 'vai toma no cú', 'vai toma no cu', 'vai tomar no rabo', 'vai toma no rabo', 'vai dar o cú', 'vai dar o cu', 'vai dar o rabo', 'filho da puta', 'filho da égua', 'filho da puta', 'filho da égua', 'filho de uma puta', 'filho de uma égua', 'filho duma puta', 'filho duma égua']
    #keywords = ['grande', 'bom', 'novo', 'pequeno', 'próprio', 'velho', 'cheio', 'branco', 'longo', 'único', 'alto', 'certo', 'só', 'possível', 'claro', 'capaz', 'estranho', 'negro', 'enorme', 'escuro', 'seguinte', 'mau', 'diferente', 'preciso', 'difícil', 'antigo', 'bonito', 'simples', 'forte', 'pobre', 'sério', 'belo', 'feliz', 'junto', 'vermelho', 'humano', 'inteiro', 'triste', 'importante', 'meio', 'sentado', 'fácil', 'verdadeiro', 'frio', 'vazio', 'baixo', 'terrível', 'próximo', 'livre', 'profundo', 'jovem', 'preto', 'impossível', 'vivo', 'largo', 'nu', 'necessário', 'azul', 'natural', 'quente', 'completo', 'verde', 'pesado', 'inglês', 'especial', 'rápido', 'igual', 'comprido', 'principal', 'breve', 'rico', 'seco', 'fino', 'geral', 'curto', 'chamado', 'pálido', 'leve', 'anterior', 'perfeito', 'grosso', 'direito', 'calado', 'interessante', 'amarelo', 'sujo', 'pronto', 'imenso', 'cansado', 'duro', 'doente', 'puro', 'presente', 'comum', 'brilhante', 'público', 'magro', 'grave', 'cego', 'deitado', 'vago', 'americano', 'alegre', 'real', 'raro', 'particular', 'calmo', 'ansioso', 'social', 'nervoso', 'má', 'silencioso', 'lento', 'semelhante', 'evidente', 'doce', 'curioso', 'normal', 'morto', 'horrível', 'familiar', 'lindo', 'caro', 'justo', 'distante', 'maravilhoso', 'inútil', 'dourado', 'gordo', 'preocupado', 'suave', 'agradável', 'pessoal', 'fraco', 'seguro', 'satisfeito', 'infeliz', 'sombrio', 'feminino', 'súbito', 'estreito', 'íntimo', 'sexual', 'interior', 'esquerdo', 'simpático', 'errado', 'contente', 'secreto', 'fresco', 'violento', 'solitário', 'político', 'moderno', 'extraordinário', 'vulgar', 'literário', 'ligeiro', 'interessado', 'eterno', 'habitual', 'falso', 'castanho', 'parado', 'inteligente', 'firme', 'misterioso', 'delicado', 'cinzento', 'intenso', 'doméstico', 'parecido', 'incapaz', 'profissional', 'disposto', 'absurdo', 'aberto', 'furioso', 'digno', 'grávido', 'amigo', 'quieto', 'físico', 'final', 'famoso', 'elegante', 'diverso', 'redondo', 'louco', 'local', 'imediato', 'provável', 'irritado', 'absoluto', 'respectivo', 'macio', 'santo', 'prestes', 'feio', 'desesperado', 'colorido', 'ridículo', 'precioso', 'imóvel', 'engraçado', 'útil', 'oposto', 'militar', 'determinado', 'britânico', 'vasto', 'religioso', 'ocupado', 'inquieto', 'impaciente', 'confuso', 'complicado', 'estúpido', 'perigoso', 'frágil', 'fechado', 'espesso', 'decidido', 'recente', 'central', 'alheio', 'agudo', 'surdo', 'minúsculo', 'húmido', 'francês', 'deserto', 'barato', 'sincero', 'sagrado', 'moral', 'luminoso', 'indiferente', 'doido', 'comercial', 'óbvio', 'obscuro', 'magnífico', 'excelente', 'inocente', 'total', 'selvagem', 'louro', 'cor-de-rosa', 'católico', 'amável', 'abafado', 'prático', 'pleno', 'infantil', 'liso', 'espantado', 'vão', 'perdido', 'grato', 'espanhol', 'divertido', 'desagradável', 'delicioso', 'consciente', 'assustado', 'português', 'mágico', 'mental', 'inferior', 'generoso', 'encantador', 'atento', 'invisível', 'industrial', 'exterior', 'estrangeiro', 'derradeiro', 'cruel', 'rígido', 'poderoso', 'modesto', 'italiano', 'gelado', 'farto', 'trémulo', 'oculto', 'nobre', 'infinito', 'inesperado', 'franco', 'encantado', 'amoroso', 'úmido', 'visível', 'severo', 'original', 'orgulhoso', 'mortal', 'esplêndido', 'coitado', 'subtil', 'constante', 'surpreendente', 'solene', 'médio', 'mudo', 'futuro', 'eléctrico', 'distinto', 'demasiado', 'culpado', 'confortável', 'banal', 'regular', 'razoável', 'molhado', 'esquisito', 'amplo', 'universitário', 'moreno', 'masculino', 'honesto', 'elevado', 'divino', 'discreto', 'confiante', 'aflito', 'zangado', 'tranquilo', 'surpreendido', 'preparado', 'miúdo', 'maldito', 'judeu', 'interno', 'insignificante', 'incrível', 'excitado', 'exacto', 'esperto', 'descalço', 'casado', 'ardente', 'típico', 'transparente', 'sólido', 'mero', 'humilde', 'doloroso', 'aéreo', 'autêntico', 'urgente', 'tenso', 'surpreso', 'sereno', 'sensível', 'querido', 'fatal', 'embaraçado', 'ruim', 'legal', 'fundo', 'contrário', 'chato', 'ausente', 'tímido', 'sinistro', 'privado', 'pensativo', 'melancólico', 'envergonhado', 'denso', 'definitivo', 'considerável', 'atrasado', 'assustador', 'artístico', 'tremendo', 'ruivo', 'mole', 'miserável', 'irritante', 'desconfiado', 'adequado', 'áspero', 'trêmulo', 'responsável', 'nítido', 'monstruoso', 'manso', 'fantástico', 'essencial', 'crescente', 'científico', 'bêbado', 'amargo', 'aliviado', 'afastado', 'telefónico', 'romântico', 'espiritual', 'cristão', 'brusco', 'apressado', 'remoto', 'insuportável', 'inicial', 'grosseiro', 'dramático', 'decente', 'admirável', 'acordado', 'sossegado', 'solteiro', 'singular', 'rouco', 'nocturno', 'loiro', 'judaico', 'irlandês', 'indignado', 'histórico', 'gracioso', 'admirado', 'supremo', 'solto', 'internacional', 'europeu', 'deprimido', 'brasileiro', 'atraente', 'animado', 'viúvo', 'ténue', 'terno', 'tamanho', 'ruidoso', 'relativo', 'penetrante', 'ordinário', 'numeroso', 'japonês', 'inúmero', 'interminável', 'ilustre', 'hesitante', 'gentil', 'feroz', 'barbudo', 'apaixonado', 'académico', 'aborrecido', 'tranqüilo', 'tradicional', 'popular', 'perturbado', 'oficial', 'limpo', 'inevitável', 'grisalho', 'extremo', 'desajeitado', 'complexo', 'artificial', 'abatido', 'virgem', 'valioso', 'sensato', 'risonho', 'piedoso', 'morno', 'metálico', 'incerto', 'idêntico', 'grego', 'gigantesco', 'fiel', 'excitante', 'esguio', 'célebre', 'apertado', 'vizinho', 'vacilante', 'universal', 'saudável', 'repleto', 'perpétuo', 'pardo', 'ofegante', 'mútuo', 'lustroso', 'isolado', 'inchado', 'gasto', 'formal', 'fascinado', 'exausto', 'escasso', 'dito', 'distraído', 'desportivo', 'contínuo', 'competente', 'clássico', 'civil', 'adulto', 'adormecido', 'técnico', 'suspeito', 'sensual', 'rigoroso', 'notável', 'irregular', 'idoso', 'excessivo', 'exato', 'espantoso', 'escolar', 'erótico', 'enganado', 'bastante', 'agitado', 'actual', 'absorto', 'teatral', 'roxo', 'robusto', 'reluzente', 'nacional', 'médico', 'moço', 'legítimo', 'idiota', 'frequente', 'conveniente', 'conhecido', 'chocado', 'brando', 'apinhado', 'tonto', 'sentimental', 'rubro', 'rosado', 'primitivo', 'ocasional', 'lateral', 'intelectual', 'horrorizado', 'devido', 'desgraçado', 'demorado', 'corrente', 'automático', 'triunfante', 'soturno', 'sorridente', 'radical', 'policial', 'perturbador', 'perplexo', 'perfumado', 'ocidental', 'monótono', 'lúgubre', 'intacto', 'indiano', 'impressionado', 'hebraico', 'exagerado', 'escarlate', 'devoto', 'constrangido', 'carregado', 'bizarro', 'aparente', 'variado', 'trágico', 'maduro', 'irónico', 'injusto', 'indeciso', 'ideal', 'heróico', 'favorável', 'débil', 'cultural', 'corajoso', 'concentrado', 'comovido', 'clandestino', 'ameaçador', 'alvo', 'vibrante', 'turístico', 'temporário', 'simbólico', 'sarcástico', 'respeitável', 'repentino', 'quadrado', 'preferível', 'ousado', 'oriental', 'negativo', 'lívido', 'límpido', 'insensível', 'grandioso', 'fatigado', 'existente', 'escondido', 'característico', 'alemão', 'sábio', 'sonoro', 'significativo', 'secundário', 'rude', 'repugnante', 'recto', 'prateado', 'podre', 'murcho', 'medieval', 'longínquo', 'intrigado', 'imperioso', 'hábil', 'formoso', 'fascinante', 'extenso', 'estridente', 'específico', 'embaraçoso', 'diário', 'disponível', 'cômico', 'cru', 'correcto', 'convencido', 'careca', 'agressivo', 'africano', 'vagaroso', 'sórdido', 'suado', 'satisfatório', 'prudente', 'obstante', 'natal', 'mesquinho', 'mecânico', 'leal', 'impressionante', 'implacável', 'horroroso', 'frouxo', 'formidável', 'fixo', 'enfadonho', 'emocional', 'económico', 'disperso', 'desvairado', 'desolado', 'dado', 'cintilante', 'afável', 'ágil', 'vistoso', 'traseiro', 'tolo', 'tardio', 'são', 'russo', 'receoso', 'prolongado', 'prodigioso', 'privilegiado', 'odioso', 'meigo', 'lógico', 'irresistível', 'intolerável', 'infernal', 'indispensável', 'habituado', 'fundamental', 'extra', 'espetado', 'escusado', 'egoísta', 'duvidoso', 'descuidado', 'convencional', 'conseguinte', 'confidencial', 'condicionado', 'cheiroso', 'cauteloso', 'atual', 'anual', 'aceitável', 'vário', 'vaidoso', 'trivial', 'tosco', 'rosa', 'ritual', 'respeitoso', 'reservado', 'propício', 'postiço', 'positivo', 'pequenino', 'pavoroso', 'patético', 'paciente', 'ondulante', 'nojento', 'musical', 'minucioso', 'maluco', 'improvável', 'glorioso', 'gigante', 'extravagante', 'exclusivo', 'esbranquiçado', 'enérgico', 'enrugado', 'direto', 'crítico', 'corpulento', 'básico', 'brutal', 'atarefado', 'arrumado', 'animal', 'ávido', 'vitoriano', 'tranquilizador', 'sonolento', 'reduzido', 'radioso', 'psicológico', 'primário', 'preferido', 'múltiplo', 'municipal', 'matinal', 'liberal', 'jovial', 'inofensivo', 'inexplicável', 'inclinado', 'iminente', 'flexível', 'financeiro', 'febril', 'entusiasmado', 'eletrônico', 'eficiente', 'directo', 'diplomático', 'diabólico', 'crucial', 'circular', 'bem-vindo', 'avermelhado', 'aterrorizado', 'aterrado', 'assírio', 'assente', 'apagado', 'ameno', 'amarelado', 'abundante', 'abjecto', 'vulnerável', 'volumoso', 'vertical', 'tácito', 'salgado', 'rasgado', 'perverso', 'permanente', 'peculiar', 'noturno', 'mórbido', 'momentâneo', 'memorável', 'maternal', 'lúcido', 'individual', 'indefinido', 'imponente', 'imperial', 'impecável', 'impassível', 'imaginário', 'hediondo', 'genial', 'fúnebre', 'exigente', 'festivo']
    #keywords = ["abbo", "abo", "abortion", "abuse", "addict", "addicts", "adult", "africa", "african", "alla", "allah", "alligatorbait", "amateur", "american", "anal", "analannie", "analsex", "angie", "angry", "anus", "arab", "arabs", "areola", "argie", "aroused", "arse", "arsehole", "asian", "ass", "assassin", "assassinate", "assassination", "assault", "assbagger", "assblaster", "assclown", "asscowboy", "asses", "assfuck", "assfucker", "asshat", "asshole", "assholes", "asshore", "assjockey", "asskiss", "asskisser", "assklown", "asslick", "asslicker", "asslover", "assman", "assmonkey", "assmunch", "assmuncher", "asspacker", "asspirate", "asspuppies", "assranger", "asswhore", "asswipe", "athletesfoot", "attack", "australian", "babe", "babies", "backdoor", "backdoorman", "backseat", "badfuck", "balllicker", "balls", "ballsack", "banging", "baptist", "barelylegal", "barf", "barface", "barfface", "bast", "bastard ", "bazongas", "bazooms", "beaner", "beast", "beastality", "beastial", "beastiality", "beatoff", "beat-off", "beatyourmeat", "beaver", "bestial", "bestiality", "bi", "biatch", "bible", "bicurious", "bigass", "bigbastard", "bigbutt", "bigger", "bisexual", "bi-sexual", "bitch", "bitcher", "bitches", "bitchez", "bitchin", "bitching", "bitchslap", "bitchy", "biteme", "black", "blackman", "blackout", "blacks", "blind", "blow", "blowjob", "boang", "bogan", "bohunk", "bollick", "bollock", "bomb", "bombers", "bombing", "bombs", "bomd", "bondage", "boner", "bong", "boob", "boobies", "boobs", "booby", "boody", "boom", "boong", "boonga", "boonie", "booty", "bootycall", "bountybar", "bra", "brea5t", "breast", "breastjob", "breastlover", "breastman", "brothel", "bugger", "buggered", "buggery", "bullcrap", "bulldike", "bulldyke", "bullshit", "bumblefuck", "bumfuck", "bunga", "bunghole", "buried", "burn", "butchbabes", "butchdike", "butchdyke", "butt", "buttbang", "butt-bang", "buttface", "buttfuck", "butt-fuck", "buttfucker", "butt-fucker", "buttfuckers", "butt-fuckers", "butthead", "buttman", "buttmunch", "buttmuncher", "buttpirate", "buttplug", "buttstain", "byatch", "cacker", "cameljockey", "cameltoe", "canadian", "cancer", "carpetmuncher", "carruth", "catholic", "catholics", "cemetery", "chav", "cherrypopper", "chickslick", "children's", "chin", "chinaman", "chinamen", "chinese", "chink", "chinky", "choad", "chode", "christ", "christian", "church", "cigarette", "cigs", "clamdigger", "clamdiver", "clit", "clitoris", "clogwog", "cocaine", "cock", "cockblock", "cockblocker", "cockcowboy", "cockfight", "cockhead", "cockknob", "cocklicker", "cocklover", "cocknob", "cockqueen", "cockrider", "cocksman", "cocksmith", "cocksmoker", "cocksucer", "cocksuck ", "cocksucked ", "cocksucker", "cocksucking", "cocktail", "cocktease", "cocky", "cohee", "coitus", "color", "colored", "coloured", "commie", "communist", "condom", "conservative", "conspiracy", "coolie", "cooly", "coon", "coondog", "copulate", "cornhole", "corruption", "cra5h", "crabs", "crack", "crackpipe", "crackwhore", "crack-whore", "crap", "crapola", "crapper", "crappy", "crash", "creamy", "crime", "crimes", "criminal", "criminals", "crotch", "crotchjockey", "crotchmonkey", "crotchrot", "cum", "cumbubble", "cumfest", "cumjockey", "cumm", "cummer", "cumming", "cumquat", "cumqueen", "cumshot", "cunilingus", "cunillingus", "cunn", "cunnilingus", "cunntt", "cunt", "cunteyed", "cuntfuck", "cuntfucker", "cuntlick ", "cuntlicker ", "cuntlicking ", "cuntsucker", "cybersex", "cyberslimer", "dago", "dahmer", "dammit", "damn", "damnation", "damnit", "darkie", "darky", "datnigga", "dead", "deapthroat", "death", "deepthroat", "defecate", "dego", "demon", "deposit", "desire", "destroy", "deth", "devil", "devilworshipper", "dick", "dickbrain", "dickforbrains", "dickhead", "dickless", "dicklick", "dicklicker", "dickman", "dickwad", "dickweed", "diddle", "die", "died", "dies", "dike", "dildo", "dingleberry", "dink", "dipshit", "dipstick", "dirty", "disease", "diseases", "disturbed", "dive", "dix", "dixiedike", "dixiedyke", "doggiestyle", "doggystyle", "dong", "doodoo", "doo-doo", "doom", "dope", "dragqueen", "dragqween", "dripdick", "drug", "drunk", "drunken", "dumb", "dumbass", "dumbbitch", "dumbfuck", "dyefly", "dyke", "easyslut", "eatballs", "eatme", "eatpussy", "ecstacy", "ejaculate", "ejaculated", "ejaculating ", "ejaculation", "enema", "enemy", "erect", "erection", "ero", "escort", "ethiopian", "ethnic", "european", "evl", "excrement", "execute", "executed", "execution", "executioner", "explosion", "facefucker", "faeces", "fag", "fagging", "faggot", "fagot", "failed", "failure", "fairies", "fairy", "faith", "fannyfucker", "fart", "farted ", "farting ", "farty ", "fastfuck", "fat", "fatah", "fatass", "fatfuck", "fatfucker", "fatso", "fckcum", "fear", "feces", "felatio ", "felch", "felcher", "felching", "fellatio", "feltch", "feltcher", "feltching", "fetish", "fight", "filipina", "filipino", "fingerfood", "fingerfuck ", "fingerfucked ", "fingerfucker ", "fingerfuckers", "fingerfucking ", "fire", "firing", "fister", "fistfuck", "fistfucked ", "fistfucker ", "fistfucking ", "fisting", "flange", "flasher", "flatulence", "floo", "flydie", "flydye", "fok", "fondle", "footaction", "footfuck", "footfucker", "footlicker", "footstar", "fore", "foreskin", "forni", "fornicate", "foursome", "fourtwenty", "fraud", "freakfuck", "freakyfucker", "freefuck", "fu", "fubar", "fuc", "fucck", "fuck", "fucka", "fuckable", "fuckbag", "fuckbuddy", "fucked", "fuckedup", "fucker", "fuckers", "fuckface", "fuckfest", "fuckfreak", "fuckfriend", "fuckhead", "fuckher", "fuckin", "fuckina", "fucking", "fuckingbitch", "fuckinnuts", "fuckinright", "fuckit", "fuckknob", "fuckme ", "fuckmehard", "fuckmonkey", "fuckoff", "fuckpig", "fucks", "fucktard", "fuckwhore", "fuckyou", "fudgepacker", "fugly", "fuk", "fuks", "funeral", "funfuck", "fungus", "fuuck", "gangbang", "gangbanged ", "gangbanger", "gangsta", "gatorbait", "gay", "gaymuthafuckinwhore", "gaysex ", "geez", "geezer", "geni", "genital", "german", "getiton", "gin", "ginzo", "gipp", "girls", "givehead", "glazeddonut", "gob", "god", "godammit", "goddamit", "goddammit", "goddamn", "goddamned", "goddamnes", "goddamnit", "goddamnmuthafucker", "goldenshower", "gonorrehea", "gonzagas", "gook", "gotohell", "goy", "goyim", "greaseball", "gringo", "groe", "gross", "grostulation", "gubba", "gummer", "gun", "gyp", "gypo", "gypp", "gyppie", "gyppo", "gyppy", "hamas", "handjob", "hapa", "harder", "hardon", "harem", "headfuck", "headlights", "hebe", "heeb", "hell", "henhouse", "heroin", "herpes", "heterosexual", "hijack", "hijacker", "hijacking", "hillbillies", "hindoo", "hiscock", "hitler", "hitlerism", "hitlerist", "hiv", "ho", "hobo", "hodgie", "hoes", "hole", "holestuffer", "homicide", "homo", "homobangers", "homosexual", "honger", "honk", "honkers", "honkey", "honky", "hook", "hooker", "hookers", "hooters", "hore", "hork", "horn", "horney", "horniest", "horny", "horseshit", "hosejob", "hoser", "hostage", "hotdamn", "hotpussy", "hottotrot", "hummer", "husky", "hussy", "hustler", "hymen", "hymie", "iblowu", "idiot", "ikey", "illegal", "incest", "insest", "intercourse", "interracial", "intheass", "inthebuff", "israel", "israeli", "israel's", "italiano", "itch", "jackass", "jackoff", "jackshit", "jacktheripper", "jade", "jap", "japanese", "japcrap", "jebus", "jeez", "jerkoff", "jesus", "jesuschrist", "jew", "jewish", "jiga", "jigaboo", "jigg", "jigga", "jiggabo", "jigger ", "jiggy", "jihad", "jijjiboo", "jimfish", "jism", "jiz ", "jizim", "jizjuice", "jizm ", "jizz", "jizzim", "jizzum", "joint", "juggalo", "jugs", "junglebunny", "kaffer", "kaffir", "kaffre", "kafir", "kanake", "kid", "kigger", "kike", "kill", "killed", "killer", "killing", "kills", "kink", "kinky", "kissass", "kkk", "knife", "knockers", "kock", "kondum", "koon", "kotex", "krap", "krappy", "kraut", "kum", "kumbubble", "kumbullbe", "kummer", "kumming", "kumquat", "kums", "kunilingus", "kunnilingus", "kunt", "ky", "kyke", "lactate", "laid", "lapdance", "latin", "lesbain", "lesbayn", "lesbian", "lesbin", "lesbo", "lez", "lezbe", "lezbefriends", "lezbo", "lezz", "lezzo", "liberal", "libido", "licker", "lickme", "lies", "limey", "limpdick", "limy", "lingerie", "liquor", "livesex", "loadedgun", "lolita", "looser", "loser", "lotion", "lovebone", "lovegoo", "lovegun", "lovejuice", "lovemuscle", "lovepistol", "loverocket", "lowlife", "lsd", "lubejob", "lucifer", "luckycammeltoe", "lugan", "lynch", "macaca", "mad", "mafia", "magicwand", "mams", "manhater", "manpaste", "marijuana", "mastabate", "mastabater", "masterbate", "masterblaster", "mastrabator", "masturbate", "masturbating", "mattressprincess", "meatbeatter", "meatrack", "meth", "mexican", "mgger", "mggor", "mickeyfinn", "mideast", "milf", "minority", "mockey", "mockie", "mocky", "mofo", "moky", "moles", "molest", "molestation", "molester", "molestor", "moneyshot", "mooncricket", "mormon", "moron", "moslem", "mosshead", "mothafuck", "mothafucka", "mothafuckaz", "mothafucked ", "mothafucker", "mothafuckin", "mothafucking ", "mothafuckings", "motherfuck", "motherfucked", "motherfucker", "motherfuckin", "motherfucking", "motherfuckings", "motherlovebone", "muff", "muffdive", "muffdiver", "muffindiver", "mufflikcer", "mulatto", "muncher", "munt", "murder", "murderer", "muslim", "naked", "narcotic", "nasty", "nastybitch", "nastyho", "nastyslut", "nastywhore", "nazi", "necro", "negro", "negroes", "negroid", "negro's", "nig", "niger", "nigerian", "nigerians", "nigg", "nigga", "niggah", "niggaracci", "niggard", "niggarded", "niggarding", "niggardliness", "niggardliness's", "niggardly", "niggards", "niggard's", "niggaz", "nigger", "niggerhead", "niggerhole", "niggers", "nigger's", "niggle", "niggled", "niggles", "niggling", "nigglings", "niggor", "niggur", "niglet", "nignog", "nigr", "nigra", "nigre", "nip", "nipple", "nipplering", "nittit", "nlgger", "nlggor", "nofuckingway", "nook", "nookey", "nookie", "noonan", "nooner", "nude", "nudger", "nuke", "nutfucker", "nymph", "ontherag", "oral", "orga", "orgasim ", "orgasm", "orgies", "orgy", "osama", "paki", "palesimian", "palestinian", "pansies", "pansy", "panti", "panties", "payo", "pearlnecklace", "peck", "pecker", "peckerwood", "pee", "peehole", "pee-pee", "peepshow", "peepshpw", "pendy", "penetration", "peni5", "penile", "penis", "penises", "penthouse", "period", "perv", "phonesex", "phuk", "phuked", "phuking", "phukked", "phukking", "phungky", "phuq", "pi55", "picaninny", "piccaninny", "pickaninny", "piker", "pikey", "piky", "pimp", "pimped", "pimper", "pimpjuic", "pimpjuice", "pimpsimp", "pindick", "piss", "pissed", "pisser", "pisses ", "pisshead", "pissin ", "pissing", "pissoff ", "pistol", "pixie", "pixy", "playboy", "playgirl", "pocha", "pocho", "pocketpool", "pohm", "polack", "pom", "pommie", "pommy", "poo", "poon", "poontang", "poop", "pooper", "pooperscooper", "pooping", "poorwhitetrash", "popimp", "porchmonkey", "porn", "pornflick", "pornking", "porno", "pornography", "pornprincess", "pot", "poverty", "premature", "pric", "prick", "prickhead", "primetime", "propaganda", "pros", "prostitute", "protestant", "pu55i", "pu55y", "pube", "pubic", "pubiclice", "pud", "pudboy", "pudd", "puddboy", "puke", "puntang", "purinapricness", "puss", "pussie", "pussies", "pussy", "pussycat", "pussyeater", "pussyfucker", "pussylicker", "pussylips", "pussylover", "pussypounder", "pusy", "quashie", "queef", "queer", "quickie", "quim", "ra8s", "rabbi", "racial", "racist", "radical", "radicals", "raghead", "randy", "rape", "raped", "raper", "rapist", "rearend", "rearentry", "rectum", "redlight", "redneck", "reefer", "reestie", "refugee", "reject", "remains", "rentafuck", "republican", "rere", "retard", "retarded", "ribbed", "rigger", "rimjob", "rimming", "roach", "robber", "roundeye", "rump", "russki", "russkie", "sadis", "sadom", "samckdaddy", "sandm", "sandnigger", "satan", "scag", "scallywag", "scat", "schlong", "screw", "screwyou", "scrotum", "scum", "semen", "seppo", "servant", "sex", "sexed", "sexfarm", "sexhound", "sexhouse", "sexing", "sexkitten", "sexpot", "sexslave", "sextogo", "sextoy", "sextoys", "sexual", "sexually", "sexwhore", "sexy", "sexymoma", "sexy-slim", "shag", "shaggin", "shagging", "shat", "shav", "shawtypimp", "sheeney", "shhit", "shinola", "shit", "shitcan", "shitdick", "shite", "shiteater", "shited", "shitface", "shitfaced", "shitfit", "shitforbrains", "shitfuck", "shitfucker", "shitfull", "shithapens", "shithappens", "shithead", "shithouse", "shiting", "shitlist", "shitola", "shitoutofluck", "shits", "shitstain", "shitted", "shitter", "shitting", "shitty ", "shoot", "shooting", "shortfuck", "showtime", "sick", "sissy", "sixsixsix", "sixtynine", "sixtyniner", "skank", "skankbitch", "skankfuck", "skankwhore", "skanky", "skankybitch", "skankywhore", "skinflute", "skum", "skumbag", "slant", "slanteye", "slapper", "slaughter", "slav", "slave", "slavedriver", "sleezebag", "sleezeball", "slideitin", "slime", "slimeball", "slimebucket", "slopehead", "slopey", "slopy", "slut", "sluts", "slutt", "slutting", "slutty", "slutwear", "slutwhore", "smack", "smackthemonkey", "smut", "snatch", "snatchpatch", "snigger", "sniggered", "sniggering", "sniggers", "snigger's", "sniper", "snot", "snowback", "snownigger", "sob", "sodom", "sodomise", "sodomite", "sodomize", "sodomy", "sonofabitch", "sonofbitch", "sooty", "sos", "soviet", "spaghettibender", "spaghettinigger", "spank", "spankthemonkey", "sperm", "spermacide", "spermbag", "spermhearder", "spermherder", "spic", "spick", "spig", "spigotty", "spik", "spit", "spitter", "splittail", "spooge", "spreadeagle", "spunk", "spunky", "squaw", "stagg", "stiffy", "strapon", "stringer", "stripclub", "stroke", "stroking", "stupid", "stupidfuck", "stupidfucker", "suck", "suckdick", "sucker", "suckme", "suckmyass", "suckmydick", "suckmytit", "suckoff", "suicide", "swallow", "swallower", "swalow", "swastika", "sweetness", "syphilis", "taboo", "taff", "tampon", "tang", "tantra", "tarbaby", "tard", "teat", "terror", "terrorist", "teste", "testicle", "testicles", "thicklips", "thirdeye", "thirdleg", "threesome", "threeway", "timbernigger", "tinkle", "tit", "titbitnipply", "titfuck", "titfucker", "titfuckin", "titjob", "titlicker", "titlover", "tits", "tittie", "titties", "titty", "tnt", "toilet", "tongethruster", "tongue", "tonguethrust", "tonguetramp", "tortur", "torture", "tosser", "towelhead", "trailertrash", "tramp", "trannie", "tranny", "transexual", "transsexual", "transvestite", "triplex", "trisexual", "trojan", "trots", "tuckahoe", "tunneloflove", "turd", "turnon", "twat", "twink", "twinkie", "twobitwhore", "uck", "uk", "unfuckable", "upskirt", "uptheass", "upthebutt", "urinary", "urinate", "urine", "usama", "uterus", "vagina", "vaginal", "vatican", "vibr", "vibrater", "vibrator", "vietcong", "violence", "virgin", "virginbreaker", "vomit", "vulva", "wab", "wank", "wanker", "wanking", "waysted", "weapon", "weenie", "weewee", "welcher", "welfare", "wetb", "wetback", "wetspot", "whacker", "whash", "whigger", "whiskey", "whiskeydick", "whiskydick", "whit", "whitenigger", "whites", "whitetrash", "whitey", "whiz", "whop", "whore", "whorefucker", "whorehouse", "wigger", "willie", "williewanker", "willy", "wn", "wog", "women's", "wop", "wtf", "wuss", "wuzzie", "xtc", "xxx", "yankee", "yellowman", "zigabo", "zipperhead"]
    #keywords = ['adorable', 'beautiful', 'clean', 'drab', 'elegant', 'fancy', 'glamorous', 'handsome', 'long', 'magnificent', 'old-fashioned', 'plain', 'quaint', 'sparkling', 'ugliest', 'unsightly', 'wide-eyed', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'gray', 'black', 'white', 'alive', 'better', 'careful', 'clever', 'dead', 'easy', 'famous', 'gifted', 'helpful', 'important', 'inexpensive', 'mushy', 'odd', 'powerful', 'rich', 'shy', 'tender', 'uninterested', 'vast', 'wrong', 'angry', 'bewildered', 'clumsy', 'defeated', 'embarrassed', 'fierce', 'grumpy', 'helpless', 'itchy', 'jealous', 'lazy', 'mysterious', 'nervous', 'obnoxious', 'panicky', 'repulsive', 'scary', 'thoughtless', 'uptight', 'worried', 'agreeable', 'brave', 'calm', 'delightful', 'eager', 'faithful', 'gentle', 'happy', 'jolly', 'kind', 'lively', 'nice', 'obedient', 'proud', 'relieved', 'silly', 'thankful', 'victorious', 'witty', 'zealous', 'broad', 'chubby', 'crooked', 'curved', 'deep', 'flat', 'high', 'hollow', 'low', 'narrow', 'round', 'shallow', 'skinny', 'square', 'steep', 'straight', 'wide', 'big', 'colossal', 'fat', 'gigantic', 'great', 'huge', 'immense', 'large', 'little', 'mammoth', 'massive', 'miniature', 'petite', 'puny', 'scrawny', 'short', 'small', 'tall', 'teeny', 'teeny-tiny', 'tiny', 'cooing', 'deafening', 'faint', 'hissing', 'loud', 'melodic', 'noisy', 'purring', 'quiet', 'raspy', 'screeching', 'thundering', 'voiceless', 'whispering', 'ancient', 'brief', 'early', 'fast', 'late', 'long', 'modern', 'old', 'old-fashioned', 'quick', 'rapid', 'short', 'slow', 'swift', 'young', 'bitter', 'delicious', 'fresh', 'greasy', 'juicy', 'hot', 'icy', 'loose', 'melted', 'nutritious', 'prickly', 'rainy', 'rotten', 'salty', 'sticky', 'strong', 'sweet', 'tart', 'tasteless', 'uneven', 'weak', 'wet', 'wooden', 'yummy', 'boiling', 'breeze', 'broken', 'bumpy', 'chilly', 'cold', 'cool', 'creepy', 'crooked', 'cuddly', 'curly', 'damaged', 'damp', 'dirty', 'dry', 'dusty', 'filthy', 'flaky', 'fluffy', 'freezing', 'hot', 'warm', 'wet', 'abundant', 'empty', 'few', 'full', 'heavy', 'light', 'many', 'numerous', 'sparse', 'substantial']
    #keywords = ['Du Hurensohn', 'Arschfotze', 'Arschgeige', 'Arschgesicht', 'Arschloch', 'Bloede Kuh', 'Bulle', 'Das ist mir scheißegal', 'Das war zu einfach', 'Deine Mutter schwitzt beim Kacken', 'Deine Mutter', 'Depp', 'Die Möpse', 'Dreckige Hure', 'Drecksau', 'Du Bastard', 'Du Drecksack', 'Du Fickfehler', 'Du Muschi', 'Du Schweinehund', 'Du Weichei', 'Du alte Kackbratze', 'Du arschgefickter Hurensohn', 'Du bist ein volltrottel', 'Du hässliger Ziegenficker', 'Du kannst mich mal', 'Du verdammtes Arschloch', 'Dumme Schlampe', 'Dummes Huhn', 'Dummkopf', 'Fick deine Mutter', 'Fick dich Arschloch', 'Fick dich ins Knie', 'Fick dich', 'Ficker', 'Fotze', 'Geh Staub fressen', 'Geh zum Teufel', 'Geh kacken', 'Gottverdammt ', 'Halt deine Fresse', 'Halt die Fresse', 'Hirnlose Ochse', 'Huhrensohn', 'Hurensohn', 'Ich Liebe Dich', 'Ich ficke deine Schwester', 'Ich hasse dich', 'Ich will dich ficken', 'Ich will ficken', 'Kackbratze', 'LMS', 'Lutsch mein Schwanz', 'Leck mich am Arsch', 'Luder', 'Lutsch meine Eier', 'Mieser Stricher', 'Mutterficker', 'Nutle', 'Nuttensohn', 'Onanieren', 'Scheissen', 'Scheiße', 'Scheißhaus', 'Schlampe', 'Schwanzlutscher', 'Schweinepriester', 'Schwuchtel', 'Schwul', 'Sheisse', 'Trottel', 'Veganer', 'Verdammte Scheiße', 'Verpiss dich', 'Wichser', 'Wixer', 'Zeig mir deine Pflaume', 'Zicke', 'Zickig', 'blutige Sau', 'bumsen', 'das Arschloch', 'der Arsch', 'der Schwanz', 'der Teufel', 'der abschaum', 'der abschaum der menschlichen gesellschaft', 'der drecksack', 'der dreckskerl', 'der schwanz', 'der schwanzlutscher', 'die Fotze', 'die Hure', 'die Scheiße', 'die Schlampe', 'die Titten', 'du blöde stinkfotze', 'du dumme kuh', 'du verdammter Arschficker', 'dumme Kuh', 'duncauf', 'fahr zur holle', 'fick dich', 'fickdich', 'homofuerst', 'ich fick deine mutter', 'ich will dich ficken', 'missgeburt', 'muschi lecker', 'verdammt du hurensohn', 'verpiss dich', 'voegeln', 'vögeln', 'wichser', 'zur Holle mit dir']
    #keywords += ['Phrase', 'abenteuerlich', 'abhängig', 'abwesend', 'aggressiv', 'ahnungslos', 'aktiv', 'allein', 'altmodisch', 'anpassungsfähig', 'anständig', 'ärgerlich', 'arm', 'arrogant', 'attraktiv', 'ätzend', 'aufgeklärt', 'aufgeregt', 'aufgeschlossen', 'aufrichtig', 'ausgeflippt', 'begabt', 'begeistert', 'bekannt', 'berühmt', 'beliebt', 'populär', 'bequem', 'bescheiden', 'bescheuert', 'bezaubernd', 'billig', 'blöd', 'boshaft', 'brav', 'charmant', 'cool', 'dankbar', 'dick', 'dumm', 'doof', 'dünn', 'egozentrisch', 'ehrgeizig', 'ehrlich', 'eifersüchtig', 'einfach', 'eingebildet', 'einmalig', 'einsam', 'einverstanden', 'ekelhaft', 'eklig', 'elegant', 'empfindlich', 'engagiert', 'engstirnig', 'erfolgreich', 'ernst', 'erstklassig', 'fair', 'falsch', 'fantastisch', 'faszinierend', 'faul', 'feig', 'fein', 'fest', 'fett', 'fit', 'fleißig', 'fortgeschritten', 'frech', 'frei', 'freundlich', 'froh', 'fröhlich', 'fürsorglich', 'gastfreundlich', 'gebildet', 'geduldig', 'gefährlich', 'gefühlvoll', 'geistreich', 'geizig', 'gemein', 'gemütlich', 'genial', 'gerecht', 'geschätzt', 'gescheit', 'geschickt', 'geschlossen', 'geschwätzig', 'gesellig', 'gesund', 'gierig', 'glaubwürdig', 'glücklich', 'grob', 'grosszügig', 'groß', 'grüntig', 'gut', 'gut angezogen', 'gut gelaunt', 'gut informiert', 'halb', 'halsstarrig', 'hart', 'hartnäckig', 'hässlich', 'heiß', 'heiter', 'hell', 'hemmungslos', 'herrlich', 'herzlos', 'hilfreich', 'hinterlistig', 'hoch', 'hochmütig', 'hochnäsig', 'höflich', 'hübsch', 'hungrig', 'idealistisch', 'intelligent', 'interessant', 'intolerant', 'jung', 'kalt', 'kindisch', 'klasse', 'toll', 'super', 'klein', 'kleinlich', 'klug', 'komisch', 'kompliziert', 'konsequent', 'konservativ', 'kontaktfreudig', 'kräftig', 'krank', 'kreativ', 'kritisch', 'krumm', 'labil', 'lang', 'langsam', 'langweilig', 'lässig', 'launisch', 'laut', 'lebendig', 'leicht', 'leichtsinnig', 'leidenschaftlich', 'leise', 'liberal', 'lieb', 'liebenswürdig', 'lustig', 'melancholisch', 'merkwürdig', 'miserabel', 'misstrauisch', 'modern', 'modisch', 'mollig', 'moralisch', 'munter', 'musikalisch', 'mutig', 'nachlässig', 'nah', 'naß', 'neidisch', 'nervös', 'nett', 'neu', 'neugierig', 'niedergeschlagen', 'niedlich', 'niedrig', 'normal', 'oberflächlich', 'offen', 'optimistisch', 'ordentlich', 'passiv', 'parteiisch', 'peinlich', 'pessimistisch', 'praktisch', 'pünktlich', 'radikal', 'raffiniert', 'rauh', 'rebellisch', 'recht', 'rechthaberisch', 'redlich', 'reich', 'reif', 'religiös', 'richtig', 'riesig', 'romantisch', 'rücksichtslos', 'rücksichtsvoll', 'ruhig', 'sauber', 'sauer', 'schick', 'schlampig', 'schlau', 'schlecht', 'schlimm', 'schmutzig', 'schnell', 'schön', 'schüchtern', 'schwach', 'schwer', 'schwierig', 'schwerfällig', 'schwermütig', 'selbstlos', 'selbstsicher', 'selbstsüchtig', 'seltsam', 'sensibel', 'sicher', '"sorgenlos', 'sorgfältig', 'spät', 'spontan', 'sportlich', 'spöttisch', 'stark', 'stolz (auf)', 'streitsüchtig', 'süß', 'sympathisch', 'taktlos', 'taktvoll', 'temperamentvoll', 'teuer', 'tot', 'traurig', 'treu', 'typisch', 'übergeschnappt', 'umweltbewusst', 'unabhängig', 'unbeholfen', 'unbekümmert', 'unberechenbar', 'unbeugsam', 'unerfarhren', 'ungehorsam', 'ungeschickt', 'unhöflich', 'unwiderstehlich', 'verantwortlich', 'verbissen', 'verdrießlich', 'verlässlich', 'verlegen', 'vernünftig', 'verrückt', 'vertrauenswürdig', 'verwirrt', 'verwöhnt', 'verzweifelt', 'vorsichtig', 'wahnsinnig', 'warm', 'warmherzig', 'wichtig', 'widerlich', 'wild', 'winzig', 'witzig', 'wunderbar', 'wunderschön', 'zerstreut', 'zufällig', 'zufrieden', 'zusammen', 'zuverlässig']
    #keywords += ['ehrgeizig', 'Amerikaner', 'ärgerlich', 'schlecht', 'schön', 'groß', 'blondine', 'langweilig', 'tapfer', 'unbesonnen', 'vorsichtig', 'bestimmt', 'charmant', 'fröhlich', 'Chinesisch', 'eingebildet', 'herkömmlich', 'feigling', 'Nüsse', 'grausam', 'schwierig', 'unangenehm', 'langweilig', 'leicht', 'Englisch', 'unecht', 'Fett', 'ein wenig', 'Französisch', 'häufig', 'freundlich', 'amüsant', 'komisch', 'General', 'großzügig', 'Deutsch', 'gut', 'hübsch', 'fleißig', 'hoch', 'ehrlich', 'intelligent', 'interessant', 'Art', 'entspannend', 'faul', 'klein', 'kurz', 'niedrig', 'bescheiden', 'launisch', 'naiv', 'engstirnig', 'neu', 'nett', 'alt', 'vollkommen', 'Persönlicher', 'fromm', 'höflich', 'schlecht', 'möglich', 'ziemlich', 'stolz', 'schnell', 'realistisch', 'neu', 'zuverlässig', 'reich', 'jämmerlich', 'egoistisch', 'empfindlich', 'schüchtern', 'stumm', 'dünn', 'schlank', 'langsam', 'klein', 'Spanisch', 'streng', 'stark', 'störrisch', 'gesprächig', 'vertrauenswürdig', 'hässlich', 'verschieden', 'schwach', 'unheimlich', 'weiß', 'jung']
    lang = 'de'
    #lang = 'en'
    #lang = 'pt'

    time = datetime.now().time()
    print(time)

    error = []
    x = 0

    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_language(lang) # we want to see German tweets only
        tso.set_include_entities(False) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts1 = TwitterSearch(
            consumer_key = 'kTs2YF5jFUZwRwnfprYMmtHc4',
            consumer_secret = 'ivn8IIaf9EByQgZ4wgvAU2nERl4J3uiuqziRWTg71ZnwOqKt3S',
            access_token = '1323543967-Ws0vHHW5CC2MlGHYDvY8oFsrLEisLucl4kJ8PlO',
            access_token_secret = 'WEQZDmz50jFmg81fjUcRQWUyPOCIUcxiWGez2UF1skk45',
         )


        ts2 = TwitterSearch(
            consumer_key = 'KTlBBJPbcphOToiXMvN0ZWAkO',
            consumer_secret = 'h5tOgnm8dt9c1lU21GdsSKPGNuBw1Zhhmlluo6bPiAucfDW0Fk',
            access_token = '1323543967-mmSfNBFyMtvLArmsaTdwiWsfunq4OHCwWUc472y',
            access_token_secret = 'jxEtyXlf5Gmh6S6awRgQ97TXsQxt5NUpxS4r8Ips1I4FH',
         )

        ts3 = TwitterSearch(
            consumer_key = 'edGj6kTiDU1NOtdSyHHJ6yoD4',
            consumer_secret = 'sGZmEV7xq4yx2ixwbhuBq6v1aCgRwuBF3IqIqhfYNLhWMokOML',
            access_token = '1323543967-JcSeOiXMxND46nMj3mkx43J8SB4A3GBR24Pkfx2',
            access_token_secret = 'zr19f231ZuV8D8gpo8asjnfEXI4gX0xWQ6AXk0kyMvimu',
         )


        ts4 = TwitterSearch(
            consumer_key = 'j8l5JUzvtn9FB8SBuOdtKsifE',
            consumer_secret = 'nKAEJnzgNn8G85bisr3wosZNKz61GnYZ3Nj2h8f6nLUP95K2L6',
            access_token = '1323543967-8EX0CGfWERxnmAbh3efPPaqpM0Dz1r6ZGaHTpRY',
            access_token_secret = '2Iga4V9dyvbR8AB3UmXd3NAqBinbJcMlu8PzNQhmoKS8O',
         )

        tss = [ts1, ts2, ts3, ts4]

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
        return

    for word in keywords:
        print(word)
        try:
            tso.set_keywords([word]) # let's define all words we would like to have a look for
            # this is where the fun actually starts :)
            for tweet in tss[x].search_tweets_iterable(tso):
                try:
                    Tweet.objects.create(text=tweet['text'], lang=lang)
                except:
                    pass
        except TwitterSearchException as e: # take care of all those ugly errors if there are some
            error.append(word)
            print(e)

        if x == 3:
            x = 0;
        else:
            x += 1;

        print(error)
        print(Tweet.objects.count())

    print(time)
    print(datetime.now().time())


def get_tweet_by_id():

    CONSUMER_KEY = 'j8l5JUzvtn9FB8SBuOdtKsifE'
    CONSUMER_SECRET = 'nKAEJnzgNn8G85bisr3wosZNKz61GnYZ3Nj2h8f6nLUP95K2L6'
    OAUTH_TOKEN = '1323543967-8EX0CGfWERxnmAbh3efPPaqpM0Dz1r6ZGaHTpRY'
    OAUTH_TOKEN_SECRET = '2Iga4V9dyvbR8AB3UmXd3NAqBinbJcMlu8PzNQhmoKS8O'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    tweets_id_file = open('tweets_id.csv', 'r')
    tweets_file = open('tweets.csv', 'w')
    tweets_id = list(csv.reader(tweets_id_file, delimiter=','))
    tweets = csv.writer(tweets_file)

    while tweets_id:
        print(len(tweets_id))
        try:
            tweet_id = tweets_id[0]
            tweet = api.get_status(str(tweet_id[0]))
            tweets.writerow([tweet_id[0], tweet.text, tweet_id[1]])
            del(tweets_id[0])
        except TweepError as e:
            print(tweets_id[0])
            print(e)
            error = ast.literal_eval(str(e))
            if error[0]['code'] != 88:
                del(tweets_id[0])

    tweets_id_file.close()
    tweets_file.close()


def count():
    #run: ./manage.py shell -c="from tweets.utils import dump; dump()"

    tweets = Tweet.objects.filter(lang='pt')
    words = set()
    count = 0
    for tweet in tweets:
        words = words.union(set(tweet.text.split()))
    print(len(words))


def dump_pt():
    #run: ./manage.py shell -c="from tweets.utils import dump_pt; dump_pt()"

    tweets = Tweet.objects.filter(lang='pt')
    bad_words = ['foda se', 'foda-se', 'vai te foder', 'vai se foder', 'vai te fuder', 'vai se foder', 'vai tomar no cu', 'vai toma no cu', 'vai tomar no rabo', 'vai toma no rabo', 'vai dar o cu', 'vai dar o rabo', 'filho da puta', 'filho da egua', 'filho de uma puta', 'filho de uma egua', 'filho duma puta', 'filho duma egua']

    tweets_br = open('tweets_br', 'w')
    tweets_br_pp = open('tweets_br_pp_test', 'w')

    count = 0

    for tweet in tweets:
        text = tweet.text
        text = re.sub('\n', '', text)
        tweets_br.write(text+'\n')
        text = re.sub(r'(\s|^)@([\w]+)|^RT|(https?:\/\/)?(w+\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text) + ' '
        text = normalize('NFKD',  text.lower()).encode('ASCII','ignore').decode('ASCII')
        text = re.sub("[^a-z ]", "", text)
        if len(text.split()) > 3:
            word = re.search(r'\b((\w[^\w ]){3,100}\w)', text)
            if word:
                text = re.sub(r'\b((\w[^\w ]){3,100}\w)', re.sub("\W", "", word.group()), text)
            for word in bad_words:
                text = text.replace(word, word.replace(' ', ''))
            count = count + 1
            tweets_br_pp.write(text+'\n')

    tweets_br.close()
    tweets_br_pp.close()
    print(count)


def dump_en():
    #run: ./manage.py shell -c="from tweets.utils import dump_en; dump_en()"

    tweets = Tweet.objects.filter(lang='en')

    tweets_en = open('tweets_en', 'w')
    tweets_en_pp = open('tweets_en_pp', 'w')

    count = 0

    for tweet in tweets:
        text = tweet.text
        text = re.sub('\n', '', text)
        tweets_en.write(text+'\n')
        text = re.sub(r'(\s|^)@([\w]+)|^RT|(https?:\/\/)?(w+\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)
        text = normalize('NFKD',  text.lower()).encode('ASCII','ignore').decode('ASCII')
        text = re.sub("[^a-z ]", "", text)
        if len(text.split()) > 3:
            word = re.search(r'\b((\w[^\w ]){3,100}\w)', text)
            if word:
                text = re.sub(r'\b((\w[^\w ]){3,100}\w)', re.sub("\W", "", word.group()), text)
            count = count + 1
            tweets_en_pp.write(text+'\n')

    tweets_en.close()
    tweets_en_pp.close()
    print(count)


def dump_de():
    #run: ./manage.py shell -c="from tweets.utils import dump_de; dump_de()"

    tweets = Tweet.objects.filter(lang='de')

    tweets_en = open('tweets_de', 'w')
    tweets_en_pp = open('tweets_de_pp', 'w')

    count = 0

    for tweet in tweets:
        text = tweet.text
        text = re.sub('\n', '', text)
        tweets_en.write(text+'\n')
        text = text.replace("ß", "ss")
        text = re.sub(r'(\s|^)@([\w]+)|^RT|(https?:\/\/)?(w+\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)
        text = normalize('NFKD',  text.lower()).encode('ASCII','ignore').decode('ASCII')
        text = re.sub("[^a-z ]", "", text)
        if len(text.split()) > 3:
            word = re.search(r'\b((\w[^\w ]){3,100}\w)', text)
            if word:
                text = re.sub(r'\b((\w[^\w ]){3,100}\w)', re.sub("\W", "", word.group()), text)
            count = count + 1
            tweets_en_pp.write(text+'\n')

    tweets_en.close()
    tweets_en_pp.close()
    print(count)


def pre_processing():
    # ./manage.py shell -c="from tweets.utils import pre_processing; pre_processing()"

    train_file = open('train_pp.csv', 'w')
    train = csv.writer(train_file)

    csvfile = open('train.csv')
    spamreader = csv.reader(csvfile, delimiter=',')

    for row in spamreader:
        text = row[2]
        text = re.sub(r'(\s|^)@([\w]+)|^RT|\n|(https?:\/\/)?(w+\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)
        text = normalize('NFKD',  text.lower()).encode('ASCII','ignore').decode('ASCII')
        text = re.sub("[^a-z ]", "", text)
        train.writerow([row[0], text])

    train_file.close()
    csvfile.close()


def join_tokens(tweet):
    keywords = ["arrombado", "asno", "acefalo", "babaca", "babuino", "baitola", "biba", "bixa", "bixinha", "bobo", "boquete", "borra", "bosta", "buceta", "burro", "cacete", "cadela", "cagar", "cala", "caralho", "chupe", "come", "corno", "cu", "cusao", "desgracado", "egua", "enraba", "fdp", "fiderapariga", "fidumaegua", "filhodaputa", "filhodeumaputa", "foda", "fodase", "foder", "fudido", "gay", "grelo", "idiota", "inferno", "jegue", "louco", "macaco", "mamar", "marica", "merda", "mijao", "otario", "pariu", "pau", "peidar", "pica", "pinto", "piriguete", "piroca", "piru", "porra", "puta", "quinto", "rapariga", "retardado", "rola", "siririca", "tesuda", "tomar", "vagabundo", "vaite", "veado", "velha", "viado", "xereca"]

    words = tweet.split()

    for keyword in keywords:
        for word in words:
            d = distance(keyword, word)
            r = ratio(keyword, word)
            if d < 2 and r > 0.8:
                tweet.replace(word, keyword)
                print(word+' - '+keyword)
    #print(badword + " = " + word + " | Distance: " + str(d) + " Ratio:" + str(r))
    return tweet


def dump_wikipedia():
    # ./manage.py shell -c="from tweets.utils import dump_wikipedia; dump_wikipedia()"


    csvfile = open('attack_annotations.tsv')
    attack_annotations = csv.reader(csvfile, delimiter='\t')
    annotations = {}

    for annotation in attack_annotations:
        break

    for annotation in attack_annotations:
        if annotation[0] not in annotations:
            annotations[annotation[0]] = 'no'
        if annotation[1] == '1.0':
            annotations[annotation[0]] = 'yes'
    csvfile.close()

    csvfile = open('attack_annotated_comments.tsv')
    annotated_comments = csv.reader(csvfile, delimiter='\t')
    wikipedia_file = open('wikipedia.csv', 'w')
    wikipedia = csv.writer(wikipedia_file)

    for comment in annotated_comments:
        break

    for comment in annotated_comments:
        if comment[0] in annotations:
            text = comment[1]
            text = re.sub(r'NEWLINE_TOKEN|TAB_TOKEN', '', text)
            text = re.sub(r'(\s|^)@([\w]+)|^RT|(https?:\/\/)?(w+\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text)
            text = normalize('NFKD',  text.lower()).encode('ASCII','ignore').decode('ASCII')
            text = re.sub("[^a-z ]", "", text)
            wikipedia.writerow(["'"+text+"'", "'"+annotations[comment[0]]+"'"])

    csvfile.close()
    wikipedia_file.close()


def open_de():
    csvfile = open('ross_texto.csv')
    a = csv.reader(csvfile, delimiter=',')
    for b in a:
        print(b)
