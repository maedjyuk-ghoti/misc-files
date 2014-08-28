set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

Plugin 'airblade/vim-gitgutter' " Git gutter!
Plugin 'bling/vim-airline' " Better status line
Plugin 'edsono/vim-matchit' " Better matching with %
Plugin 'kshenoy/vim-signature' " Show off marks!
Plugin 'Lokaltog/vim-easymotion' " Super fast navigation!
Plugin 'mhinz/vim-startify' " Start menu!
Plugin 'nvie/vim-flake8' " Python static syntax and style checker
Plugin 'plasticboy/vim-markdown' " Markdown highlighting
Plugin 'scrooloose/nerdtree' " File navigation
Plugin 'scrooloose/nerdcommenter' " Easy comments
Plugin 'scrooloose/syntastic' " Syntax checker
"Plugin 'sjl/gundo.vim' " More power to the undo
Plugin 'tpope/vim-repeat' " Dot works for plugins
Plugin 'tpope/vim-surround' " Manipulate parens, quotes, etc.
Plugin 'Valloric/YouCompleteMe' " Code completion requires Vim 7.3.584+

" Colorschemes
Plugin 'tomasr/molokai'
Plugin 'pychimp/vim-luna'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

" COLORS
colorscheme luna

" AIRLINE
let g:airline#extensions#tabline#enabled = 1
let g:airline_powerline_fonts = 1 " Also fix the fonts
set laststatus=2 " Always show the airline statusbar
set noshowmode " Don't show the -- MODE -- indicator below airline
set encoding=utf-8
"let g:airline_detect_whitespace = 0 " Hide the trailing whitespace warning

" EASYMOTION
"let g:EasyMotion_do_mapping = 0 " Disable default mappings
"nmap <SP> <Plug>(easymotion-s2) " Bi-directional find motion
let g:EasyMotion_smartcase = 1 " Turn on case sensitive feature
let g:EasyMotion_enter_jump_first = 1 " Enter jumps to first match; works poorly
map <Leader>j <Plug>(easymotion-j) " Goto any line below
map <Leader>k <Plug>(easymotion-k) " Goto any line above
map  <Leader>/ <Plug>(easymotion-sn) " Indexed search
omap <Leader>/ <Plug>(easymotion-tn) " Indexed search

" STARTIFY
let g:startify_custom_header = [ 'VI VI VI THE EDITOR OF THE BEAST', '' ]
set tabstop=4
set shiftwidth=4
set expandtab
