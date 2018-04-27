/*
A KBase module: kb_BatchApp
*/

module kb_BatchApp {

    typedef string obj_ref;

    typedef structure{
        string      cell_id;
        string      run_id;
        string      tag;
    } MetaInput;

    typedef structure {
        list<mapping<string, UnspecifiedObject>> params;
        list<obj_ref>                        source_ws_objects;
    } ParamsInput;

    typedef structure{

        string      app_id;
        string      method;
        string      service_ver;
        string      wsid;
        MetaInput   meta;
        list<ParamsInput>  batch_params;
    } BatchInput;

    typedef structure{
        mapping<string, string>   batch_result;
        string      report_name;
        string      report_ref;
    } BatchResult;

    funcdef run_batch(BatchInput params)
        returns (BatchResult returnVal) authentication required;
};