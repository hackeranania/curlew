import click,time,socket,os
import requests
import tldextract
from halo import Halo
from rich.console import Console
from rich.status import Status
import validators
import nmap
from requests.exceptions import Timeout
console = Console(highlight=False)




@click.command()
@click.version_option('1.0.1\n developed by Anania belay \n kebere le dengel mariyam ena le selus kidus',help='outputs the version')

@click.option('--sdV','vuln', is_flag=True,help='Check for the subdomain  vulnerability')
@click.option('-u','mainurl',required=True,help='The main url to be feteched [max url:1]',type=str,nargs=1)
@click.option('--ip',default=False,is_flag=True,help='The ip of the server to be concluded')

@click.option('--search',required=False,help='To search specific subdomain')
@click.option('-o',is_flag=False,help='The file to be outputted',default='/')
@click.option('--proxy',required=False,help='To use proxy while searching')
@click.option('--noprint',help='To dont show output on the terminal',is_flag=True,required=False,default=False)
@click.option('-B',default='500',help='sub domains to fetch aviable values 100,500,800,1000,10000 [default:500]')
@click.option('-t',default=1,help='Timeout for the  Bruteforce[default:1]')
def win(mainurl,vuln,search,ip,o,proxy,noprint,b,t):
    
        
    if b =='100' or b=='1000' or b =='10000' or b=='500' or b=='800':
        pass
        int(b)
    else:
        console.print('[white][bold][+]InValid value of -B vaild values are in the help menu[/white][bold]')
        exit()
     

    try:
        file = open(f'subdomains/subdomains-{b}.txt')
        content = file.read()
        subdomain = content.splitlines()
       
    except FileNotFoundError:
        run = Halo(text='Download Bruteforce Files',text_color='white', spinner='dots')
        run.start()
        time.sleep(1)
        os.system('git clone https://github.com/hackeranania/subdomains')
        run.succeed('File Downloaded')

        file = open(f'subdomains/subdomains-{b}.txt')
        content = file.read()
        subdomain = content.splitlines()

    
    if  validators.url(mainurl):
        if noprint:
            if o == '/':
                console.print('[red][bold]--noprint requires the output file[/red][/bold]')
                exit()
        else:
            pass
        splitted = mainurl.split('://')
        run = Halo(text='Initalizing',text_color='blue', spinner='dots')
        run.start()
        time.sleep(2)
        run.succeed('Initialized')

        run = Halo(text='Checking for Internet access',text_color='green', spinner='dots')
        run.start()
        time.sleep(2)
  
        if Main.CheckThereIsConnection():
            run.succeed('Internet is Aviable')
        else:
            run.fail('No Internet Access') 
            exit()   
        

        run = Halo(text='Checking for The url is online',text_color='yellow', spinner='dots')
        run.start()
        time.sleep(0.5)
        try:
            main = requests.get(mainurl,timeout=t)
        except Timeout:
            main = '400'    
        if '400' in main:
            run.fail('sever is not aviable or your behind proxy') 
            exit()  
        else:
            run.succeed('Server is online')


        run = Halo(text='Checking for ssl',text_color='blue', spinner='dots')
        run.start()
        time.sleep(2)
        if splitted[0] == 'https' or splitted[0] == 'http':
            run.succeed('It uses '+ splitted[0] +' Protocol')
            # print(socket.gethostbyname(splitted[1]))
        else:
            run.fail('Unsupported protocol')
        extra = tldextract.extract(mainurl)
        
        the_valid = []
        success = 0 
        for i in subdomain:
            
            try:
                url = splitted[0]+'://'+i+'.'+extra.domain+'.'+extra.suffix
                
                requests.get(url,timeout=t)
                if noprint !=True:
                    if ip:

                        fetecher = tldextract.extract(mainurl) 
                        passed = socket.gethostbyname(fetecher.domain+'.'+fetecher.suffix) 
                        console.print(f'[green][bold]:thumbs_up:New subdomain found {url} with ip: {passed}[/green][/bold]')
                        the_valid.append(url)
                        success += 1
                    else:
                        
                        
        
        
                        console.print(f'[green][bold]:thumbs_up:New subdomain found {url}[/green][/bold]')
                        the_valid.append(url)
                        success += 1
            
                else:
                    the_valid.append(url) 
                    success += 1       
            except Timeout:
                pass
            except:
                if noprint != True:
                    console.print(f':thumbs_down:[red][bold]{url}[red][bold]')    
            
        if o == '/':
            pass 
        else:
            if ip !=True:
                try:
                    run = Halo(text=f'Writiing the data to {o}',text_color='blue', spinner='dots')
                    run.start()
        
        
                    with open(o, 'w') as f:
                        for line in the_valid:
                            f.write(line)
                            f.write('\n')
                        run.succeed(f'Write completed in to {o}')
                    console.print(f'[bold][yellow]{success} Domains are found!![yellow][bole]')
                except:
                    run.fail('May be run with sudo permission')                


            else:
                try:
                    run = Halo(text=f'Writiing the data to {o} with ip',text_color='blue', spinner='dots')
                    run.start()
        
                    with open(o, 'w') as f:
                        for line in the_valid:
                            fetecher = tldextract.extract(line) 
                            passed = socket.gethostbyname(fetecher.domain+'.'+fetecher.suffix) 

                            f.write(line+'    ip: '+ passed)
                            f.write('\n')
                        run.succeed(f'Write completed in to {o}')
                    console.print(f'[bold][yellow]{success} Domains are found!![yellow][bole]')
                except:
                    run.fail('May be run with sudo permission')

    else:
        print('Invalid url please')


class Main:
    @staticmethod              
    def CheckThereIsConnection(host="8.8.8.8", port=53,timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False
   






win()	










