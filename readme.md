# Диплом
# Разработка системы платежной транзакции

## тезисы

- Необходимо изложить историю технологии blockchain, от куда происходит, как смогли
привязать к децентрализации передачи информации, майнинг и оформить в виде crypto валюты.
Описать понятие crypto, как она используеся во всех системах ИТ, основные подходы и
развитие.
- Описать экономические модели человечества до появления криптовалюты, основные
законы экономики. Связать с децентрализацией на фоне санкций, дать обоснование выгоды
систем проведения финансовых транзакций, основные понятия, способы реализации известные
в открытых источниках, выгода.
- Описать свое видение пакета(фрейма.кадра) транзакции, что необходимо включать по
мимио технической информации. Описать минимальные требования для каналов связи,
железа ,софта для выстраивания автоматизированнной банковской системы. Основные
ППО(прикладное програмное обеспечение) БД, транспорт, шифрование, бэкапировние.
- еализовать стэнд, где необходимо показать передачу транзакционного пакета данных,
с возможностью хранения свыше 15 лет. Предоставить некое нагрузочное тестирование,
примеры внедрения и использования.
- Основываясь на экономических моделях, реалиях современного мира, обосновать
экономическую выгоду на 5-10 лет вперед. Учесть конкуренцию криптобирж, развитие computer
science, санкции от не дружественных стран.
- диск сломался отвал. куда привязать (лучшие практики).
- исторический экскурс китай тесты. назвать в каких странах есть. история.
- рассказы про майнинг регуляторы сертификаты. шлюзы. 
- что делать чтобы не проебать транзакции.
- фича что заошники ипшники гоняют между странами нет завязки на свифте и юнивепей, обмен межстранный финансами. 
- подпитываются тем что находятся у стран.
- доллар->новая крипта универсальная валюта. 
- 5 лет надо хранить фин операцию по закону.
- сколько крипты у других стран

## че надо сделать
- скидывать заметки и все подряд. 
- начинать накидывать абзацы предложения.
- посмотреть требования по диплому какие главы скок страниц стандарты посмотреть.


## описание

2. главной киллерфичей транзакций будет отсутствие комиссий за перевод монет, это решит все проблемы биткоина с усложненными транзакциями с тысячами инпутов аутпутов. Чтобы обеспечить бесплатный транзакции будет использоваться Proof-of-Authority (подойдет и как государственная валюта, где валидаторами будут какие то выбранные людьми условные комиссии по валидации, также как и безгосударственная менее централизованная ничего по сути не меняется). благодаря PoA значительно снижается расходы на электричество и технику, повышается скорость. Из минусов это менее децентрализовано чем PoS или PoW. Но зато все строится не на анонимных майнерах/холдерах а на проверенных людях/компаниях держащих ноды-валидаторы/мастерноды.

транзакция будет выглядеть как то так

```json
{
    "height": 1,
    "block_timestamp": "2023-01-01T00:00:00",
    "block_height": 100,
    "block_transaction_index": 0,
    "hash": "some_hash",
    "type": "transaction",
    "version": 1,
    "amount": 100,
    "sender_address": "sender_address",
    "sender_account_type": "sender_type",
    "sender_account_balance": 1000,
    "sender_account_transaction_count": 10,
    "recipient_amount": 50,
    "recipient_address": "recipient_address",
    "recipient_account_type": "recipient_type",
    "recipient_account_balance": 500,
    "recipient_account_transaction_count": 5,
    "timestamp": "2023-01-01T12:00:00"
}
```


тут сразу задел под разные операции (помимо перевода будет сжигание например или создание нфт, подпись документов итд)


Precision будет 2 знака после запятой, как у фиатных денег. Большая точность как мне кажется вредит пониманию и усложняет вычисления.

3. Мое видение это кратное упрощение и ускорение транзакций для простого внедрения и использования. По плану я просто напишу систему (backend+frontend) с демонстрационными возможностями разворачивания нод, отправки транзакций. Возможно еще добавлю хранение в бч каких то данных по аккаунту (к примеру можно будет нотариальную систему придумать чтобы заверять все блокчейном как надежным авторитнетным источником).


Про защиту не знаю что сказать. Расскажу мотивацию, покажу стенд, фичи и пользу для общества, перспективы внедрения.


## туду по описанию тезисов

1. Платформа инфр-ра, делай rnd, во время сессии
2. Не забудь про долго срочное хранение, HA и геораспределенные ЦОД
3. Биг дата, как СУБД с шустрым поиском. К февралю будет стенд с opensearch
4. Продумай net plan
Рез-ат "черновой" к февралю в формате doc. В почту. Уделяй по 20-30 мин в день. Отписывай шаги заворачивай в гит. Записки на полях не более, но мысль заворачивай в почту