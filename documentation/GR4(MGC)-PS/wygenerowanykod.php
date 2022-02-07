<?php
class Użytkownik 
{
    private /*object*/ $status_zalogowania;Boolean;      
    private /*object*/ $Profil;Object;      

    
    public function zarejestruj ()
    {
        
    }      
    
    public function zaloguj ()
    {
        
    }      
    
    public function wyloguj ()
    {
        
    }      
    
    public function wprowadź_piosenkę_do_systemu (/*object*/ $stringZrodlo)
    {
        
    }      
}
?>

<?php
class Piosenka 
{
    public /*object*/ $tytuł;String;      
    public /*object*/ $gatunek;String;      
    public /*object*/ $źródło;String;      

    
    public function rozpoznanie_gatunku ()
    {
        
    }      
    
    public function wyświetlenie_informacji_o_utworze ()
    {
        
    }      
    
    public function zapisanie_utworu_w_historii ()
    {
        
    }      
}
?>

<?php
class Profil 
{
    private /*object*/ $email;String;      
    private /*object*/ $nazwa_użytkownika;String;      
    private /*object*/ $hasło;String;      
    private /*object*/ $avatar;Blob;      

    
    public function edycja_profilu ()
    {
        
    }      
    
    public function usun_konto ()
    {
        
    }      
}
?>

<?php
class Historia 
{
    public /*object*/ $Piosenka;Object;      
    public /*object*/ $data;Date;      

    
    public function przegladanie_zapisanych_utworów ()
    {
        
    }      
    
    public function wyszukiwanie_w_historii ()
    {
        
    }      
}
?>

<?php
class PodobnyUtwór 
{
    public /*object*/ $Piosenka;Object;      

    
    public function wyświetlenie_podobnego_utworu ()
    {
        
    }      
}
?>

