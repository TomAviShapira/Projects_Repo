%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [] = sendMail(videoName, th, filter, bufferSize, shift)
%% send mail
    mail = 'technionprojecta@gmail.com'; %Your GMail email address
    password = 'litaltom';  %Your GMail password
    setpref('Internet','SMTP_Server','smtp.gmail.com');
    setpref('Internet','E_mail',mail);
    setpref('Internet','SMTP_Username',mail);
    setpref('Internet','SMTP_Password',password);
    props = java.lang.System.getProperties;
    props.setProperty('mail.smtp.auth','true');
    props.setProperty('mail.smtp.socketFactory.class', 'javax.net.ssl.SSLSocketFactory');
    props.setProperty('mail.smtp.socketFactory.port','465');
    msg = sprintf('%s_%s_%s_%s_%s - DONE\n',videoName, th, filter, bufferSize, shift);
    sendmail(mail,'project A simulatiom',msg)
end

