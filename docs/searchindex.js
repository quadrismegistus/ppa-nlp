Search.setIndex({docnames:["architecture","changelog","codedocs","deploynotes","index"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.todo":1,"sphinx.ext.viewcode":1,sphinx:55},filenames:["architecture.rst","changelog.rst","codedocs.rst","deploynotes.rst","index.rst"],objects:{"ppa.archive":{NO_COLLECTION_LABEL:[2,1,1,""],admin:[2,0,0,"-"],forms:[2,0,0,"-"],hathi:[2,0,0,"-"],models:[2,0,0,"-"],solr:[2,0,0,"-"],util:[2,0,0,"-"],views:[2,0,0,"-"]},"ppa.archive.admin":{CollectionAdmin:[2,2,1,""],DigitizedWorkAdmin:[2,2,1,""]},"ppa.archive.admin.DigitizedWorkAdmin":{bulk_add_collection:[2,3,1,""],get_readonly_fields:[2,3,1,""],list_collections:[2,3,1,""],save_model:[2,3,1,""],save_related:[2,3,1,""],source_link:[2,3,1,""]},"ppa.archive.forms":{AddFromHathiForm:[2,2,1,""],AddToCollectionForm:[2,2,1,""],CheckboxSelectMultipleWithDisabled:[2,2,1,""],FacetChoiceField:[2,2,1,""],ModelMultipleChoiceFieldWithEmpty:[2,2,1,""],RadioSelectWithDisabled:[2,2,1,""],RangeField:[2,2,1,""],RangeWidget:[2,2,1,""],SearchForm:[2,2,1,""],SearchWithinWorkForm:[2,2,1,""],SelectDisabledMixin:[2,2,1,""],SelectWithDisabled:[2,2,1,""]},"ppa.archive.forms.AddFromHathiForm":{get_hathi_ids:[2,3,1,""]},"ppa.archive.forms.FacetChoiceField":{valid_value:[2,3,1,""]},"ppa.archive.forms.ModelMultipleChoiceFieldWithEmpty":{clean:[2,3,1,""]},"ppa.archive.forms.RangeField":{compress:[2,3,1,""],widget:[2,4,1,""]},"ppa.archive.forms.RangeWidget":{decompress:[2,3,1,""],sep:[2,4,1,""]},"ppa.archive.forms.SearchForm":{QUESTION_POPUP_TEXT:[2,4,1,""],defaults:[2,5,1,""],get_solr_sort_field:[2,3,1,""],has_keyword_query:[2,3,1,""],pub_date_minmax:[2,3,1,""],set_choices_from_facets:[2,3,1,""]},"ppa.archive.forms.SearchWithinWorkForm":{QUESTION_POPUP_TEXT:[2,4,1,""]},"ppa.archive.hathi":{HathiBaseAPI:[2,2,1,""],HathiBibliographicAPI:[2,2,1,""],HathiBibliographicRecord:[2,2,1,""],HathiDataAPI:[2,2,1,""],HathiItemForbidden:[2,6,1,""],HathiItemNotFound:[2,6,1,""],HathiObject:[2,2,1,""],METSFile:[2,2,1,""],MinimalMETS:[2,2,1,""],StructMapPage:[2,2,1,""]},"ppa.archive.hathi.HathiBaseAPI":{api_root:[2,4,1,""]},"ppa.archive.hathi.HathiBibliographicAPI":{brief_record:[2,3,1,""],record:[2,3,1,""]},"ppa.archive.hathi.HathiBibliographicRecord":{copy_details:[2,3,1,""],copy_last_updated:[2,3,1,""],marcxml:[2,4,1,""],pub_dates:[2,4,1,""],title:[2,4,1,""]},"ppa.archive.hathi.HathiDataAPI":{get_aggregate:[2,3,1,""],get_structure:[2,3,1,""]},"ppa.archive.hathi.HathiObject":{content_dir:[2,4,1,""],delete_pairtree_data:[2,3,1,""],metsfile_path:[2,3,1,""],pairtree_client:[2,3,1,""],pairtree_id:[2,4,1,""],pairtree_object:[2,3,1,""],pairtree_prefix:[2,4,1,""],zipfile_path:[2,3,1,""]},"ppa.archive.hathi.METSFile":{id:[2,4,1,""],location:[2,4,1,""],sequence:[2,4,1,""]},"ppa.archive.hathi.MinimalMETS":{structmap_pages:[2,4,1,""]},"ppa.archive.hathi.StructMapPage":{display_label:[2,4,1,""],label:[2,4,1,""],order:[2,4,1,""],orderlabel:[2,4,1,""],text_file:[2,4,1,""],text_file_id:[2,4,1,""],text_file_location:[2,4,1,""]},"ppa.archive.management.commands":{hathi_import:[2,0,0,"-"],index:[2,0,0,"-"],solr_schema:[2,0,0,"-"]},"ppa.archive.models":{Collection:[2,2,1,""],CollectionSignalHandlers:[2,2,1,""],DigitizedWork:[2,2,1,""],NO_COLLECTION_LABEL:[2,1,1,""],ProtectedWorkField:[2,2,1,""],ProtectedWorkFieldFlags:[2,2,1,""],TrackChangesModel:[2,2,1,""]},"ppa.archive.models.Collection":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""],description:[2,4,1,""],exclude:[2,4,1,""],get_usage:[2,3,1,""],name:[2,4,1,""],name_changed:[2,4,1,""],stats:[2,5,1,""]},"ppa.archive.models.CollectionSignalHandlers":{"delete":[2,5,1,""],save:[2,5,1,""]},"ppa.archive.models.DigitizedWork":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""],add_from_hathi:[2,5,1,""],added:[2,4,1,""],clean:[2,3,1,""],collections:[2,4,1,""],compare_protected_fields:[2,3,1,""],count_pages:[2,3,1,""],display_title:[2,3,1,""],enumcron:[2,4,1,""],get_absolute_url:[2,3,1,""],get_hathi_data:[2,3,1,""],get_metadata:[2,3,1,""],has_fulltext:[2,4,1,""],hathi:[2,4,1,""],index_data:[2,3,1,""],index_id:[2,3,1,""],is_public:[2,3,1,""],is_suppressed:[2,4,1,""],notes:[2,4,1,""],page_count:[2,4,1,""],page_index_data:[2,3,1,""],populate_fields:[2,3,1,""],populate_from_bibdata:[2,3,1,""],printed_by_re:[2,4,1,""],protected_fields:[2,4,1,""],pub_place:[2,4,1,""],public_notes:[2,4,1,""],publisher:[2,4,1,""],record_id:[2,4,1,""],save:[2,3,1,""],sort_title:[2,4,1,""],source:[2,4,1,""],source_id:[2,4,1,""],source_url:[2,4,1,""],status:[2,4,1,""],subtitle:[2,4,1,""],title:[2,4,1,""],updated:[2,4,1,""]},"ppa.archive.models.ProtectedWorkField":{from_db_value:[2,3,1,""],get_prep_value:[2,3,1,""],to_python:[2,3,1,""]},"ppa.archive.models.ProtectedWorkFieldFlags":{author:[2,4,1,""],deconstruct:[2,7,1,""],enumcron:[2,4,1,""],pub_date:[2,4,1,""],pub_place:[2,4,1,""],publisher:[2,4,1,""],sort_title:[2,4,1,""],subtitle:[2,4,1,""],title:[2,4,1,""]},"ppa.archive.models.TrackChangesModel":{has_changed:[2,3,1,""],initial_value:[2,3,1,""],save:[2,3,1,""]},"ppa.archive.solr":{CoreAdmin:[2,2,1,""],Indexable:[2,2,1,""],PagedSolrQuery:[2,2,1,""],SolrSchema:[2,2,1,""],get_solr_connection:[2,8,1,""]},"ppa.archive.solr.CoreAdmin":{reload:[2,3,1,""]},"ppa.archive.solr.Indexable":{identify_index_dependencies:[2,7,1,""],index:[2,3,1,""],index_chunk_size:[2,4,1,""],index_data:[2,3,1,""],index_id:[2,3,1,""],index_items:[2,7,1,""],remove_from_index:[2,3,1,""]},"ppa.archive.solr.PagedSolrQuery":{count:[2,3,1,""],facet_ranges:[2,4,1,""],get_expanded:[2,3,1,""],get_facets:[2,3,1,""],get_highlighting:[2,3,1,""],get_json:[2,3,1,""],get_results:[2,3,1,""],raw_response:[2,4,1,""],set_limits:[2,3,1,""]},"ppa.archive.solr.SolrSchema":{fields:[2,4,1,""],solr_schema_field_types:[2,3,1,""],solr_schema_fields:[2,3,1,""],text_fields:[2,4,1,""],update_solr_schema:[2,3,1,""]},"ppa.archive.util":{HathiImporter:[2,2,1,""]},"ppa.archive.util.HathiImporter":{SKIPPED:[2,4,1,""],SUCCESS:[2,4,1,""],add_items:[2,3,1,""],filter_existing_ids:[2,3,1,""],get_status_message:[2,3,1,""],index:[2,3,1,""],output_results:[2,3,1,""],status_message:[2,4,1,""]},"ppa.archive.views":{AddFromHathiView:[2,2,1,""],AddToCollection:[2,2,1,""],DigitizedWorkByRecordId:[2,2,1,""],DigitizedWorkCSV:[2,2,1,""],DigitizedWorkDetailView:[2,2,1,""],DigitizedWorkListView:[2,2,1,""],OpenSearchDescriptionView:[2,2,1,""]},"ppa.archive.views.AddFromHathiView":{form_class:[2,4,1,""],form_valid:[2,3,1,""],get_context_data:[2,3,1,""]},"ppa.archive.views.AddToCollection":{form_class:[2,4,1,""],get_queryset:[2,3,1,""],get_success_url:[2,3,1,""],model:[2,4,1,""],post:[2,3,1,""]},"ppa.archive.views.DigitizedWorkByRecordId":{get_redirect_url:[2,3,1,""]},"ppa.archive.views.DigitizedWorkCSV":{get:[2,3,1,""],get_csv_filename:[2,3,1,""],get_data:[2,3,1,""],model:[2,4,1,""],render_to_csv:[2,3,1,""]},"ppa.archive.views.DigitizedWorkDetailView":{form_class:[2,4,1,""],get_context_data:[2,3,1,""],get_template_names:[2,3,1,""],last_modified:[2,3,1,""],model:[2,4,1,""]},"ppa.archive.views.DigitizedWorkListView":{form_class:[2,4,1,""],get_context_data:[2,3,1,""],get_page_highlights:[2,3,1,""],get_queryset:[2,3,1,""],last_modified:[2,3,1,""],meta_description:[2,4,1,""],meta_title:[2,4,1,""],model:[2,4,1,""]},"ppa.common":{admin:[2,0,0,"-"],views:[2,0,0,"-"]},"ppa.common.admin":{LocalUserAdmin:[2,2,1,""]},"ppa.common.admin.LocalUserAdmin":{group_names:[2,3,1,""]},"ppa.common.views":{AjaxTemplateMixin:[2,2,1,""],LastModifiedListMixin:[2,2,1,""],LastModifiedMixin:[2,2,1,""],VaryOnHeadersMixin:[2,2,1,""]},"ppa.common.views.AjaxTemplateMixin":{ajax_template_name:[2,4,1,""],get_template_names:[2,3,1,""],vary_headers:[2,4,1,""]},"ppa.common.views.LastModifiedMixin":{solr_timestamp_to_datetime:[2,5,1,""]},"ppa.common.views.VaryOnHeadersMixin":{dispatch:[2,3,1,""]},"ppa.editorial":{models:[2,0,0,"-"]},"ppa.editorial.models":{EditorialIndexPage:[2,2,1,""],EditorialPage:[2,2,1,""]},"ppa.editorial.models.EditorialIndexPage":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""],route:[2,3,1,""]},"ppa.editorial.models.EditorialPage":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""],set_url_path:[2,3,1,""]},"ppa.pages":{models:[2,0,0,"-"]},"ppa.pages.management.commands":{setup_site_pages:[2,0,0,"-"]},"ppa.pages.models":{BodyContentBlock:[2,2,1,""],CollectionPage:[2,2,1,""],ContentPage:[2,2,1,""],ContributorPage:[2,2,1,""],HomePage:[2,2,1,""],ImageWithCaption:[2,2,1,""],PagePreviewDescriptionMixin:[2,2,1,""],Person:[2,2,1,""]},"ppa.pages.models.CollectionPage":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""]},"ppa.pages.models.ContentPage":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""]},"ppa.pages.models.ContributorPage":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""]},"ppa.pages.models.HomePage":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""]},"ppa.pages.models.PagePreviewDescriptionMixin":{allowed_tags:[2,4,1,""],get_description:[2,3,1,""],get_plaintext_description:[2,3,1,""],max_length:[2,4,1,""]},"ppa.pages.models.Person":{DoesNotExist:[2,6,1,""],MultipleObjectsReturned:[2,6,1,""],description:[2,4,1,""],get_usage:[2,3,1,""],name:[2,4,1,""],photo:[2,4,1,""],project_role:[2,4,1,""],url:[2,4,1,""]},"ppa.unapi":{views:[2,0,0,"-"]},"ppa.unapi.views":{UnAPIView:[2,2,1,""]},"ppa.unapi.views.UnAPIView":{content_type:[2,4,1,""],file_extension:[2,4,1,""],formats:[2,4,1,""],get:[2,3,1,""],get_context_data:[2,3,1,""],get_metadata:[2,3,1,""],template_name:[2,4,1,""]},ppa:{archive:[2,0,0,"-"],common:[2,0,0,"-"],editorial:[2,0,0,"-"],pages:[2,0,0,"-"],unapi:[2,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","data","Python data"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","staticmethod","Python static method"],"6":["py","exception","Python exception"],"7":["py","classmethod","Python class method"],"8":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:data","2":"py:class","3":"py:method","4":"py:attribute","5":"py:staticmethod","6":"py:exception","7":"py:classmethod","8":"py:function"},terms:{"15z":2,"20t10":2,"21z":2,"24t09":2,"68b329da9893e34099c7d8ad5cb9c940":2,"boolean":2,"break":1,"case":[1,2],"class":2,"default":[1,2],"export":[2,4],"final":4,"float":2,"function":[0,2,3],"import":[0,4],"int":2,"long":2,"new":[0,1,2,3,4],"public":2,"return":2,"short":2,"static":[2,4],"switch":[1,3],"true":2,AND:2,CAS:1,CMS:[0,2],For:[2,3],IDs:[1,2],The:[0,1,2,3,4],Then:4,These:4,Use:[2,4],Used:2,Uses:2,Using:1,Will:2,With:2,_all_:2,abbr:2,abl:1,about:[1,2],access:[1,2,4],accomplish:4,account:1,acronym:2,across:1,activ:[1,4],actual:[1,2],adapt:2,add:[0,1,2,3,4],add_from_hathi:2,add_item:2,added:[1,2,3,4],addfromhathiform:2,addfromhathiview:2,adding:[1,3],addit:[1,2,3,4],address:3,addtocollect:2,addtocollectionform:2,adjust:1,admin:3,admin_sit:2,administr:[0,2],advanc:1,advisori:2,affili:2,after:2,against:[3,4],aggreg:2,ajax:2,ajax_template_nam:2,ajaxtemplatemixin:2,alia:2,all:[0,1,2,3,4],allow:[0,1,2,3],allowed_tag:2,alphabet:1,alreadi:[2,3],also:[1,2,3,4],altern:4,alwai:2,analysi:1,analyt:[1,3],analyz:1,ani:[1,2],anim:1,anyth:2,apach:4,api:[1,2,3],api_root:2,app:[0,2],appear:[1,2],applic:[0,2,3,4],appropri:2,architectur:4,archiv:[1,3],area:1,arg:2,argument:2,around:1,arrang:1,articl:[1,2],asset:4,assign:1,associ:[1,2],assum:[2,3],attr:2,attr_nam:2,attribut:[1,2],auth:2,author:[1,2],author_exact:2,authorship:2,auto_id:2,autom:4,automat:[1,3,4],avail:[1,2,4],avoid:[2,3],awar:1,back:[1,2],bad:1,badg:1,bar:[2,3],base:[0,1,2],bash:4,basic:[0,2,3],basic_config:3,becaus:[2,3],been:[2,3],befor:[2,3,4],begin:2,behavior:2,being:1,belong:[1,2],benefit:3,better:1,bib_api:2,bibdata:2,bibliograph:[0,1,2],bin:4,bleach:2,block:[1,2],blockquot:2,blog:[1,2],board:[2,3],bodi:2,bodycontentblock:2,boost:[1,3],both:[0,2],branch:4,brief:[1,2],brief_record:2,broken:[1,3],brows:[0,1,2],browser:[1,2],bugfix:1,build:4,built:1,bulk:[2,4],bulk_add_collect:2,button:1,cach:2,calcul:2,call:[2,4],can:[1,2,4],cannot:3,capit:2,caption:[1,2],catalog:[1,2],caus:1,cdh:[1,4],certain:1,chang:[1,2,3,4],change_list:2,charact:2,charter:1,check:[1,2],checkboxselect:2,checkboxselectmultipl:2,checkboxselectmultiplewithdis:2,checksum:2,checksumtyp:2,choic:2,chrome:1,chronolog:2,chunk:2,citat:1,clarifi:1,classmethod:2,clean:[1,2,3],clear:[1,2,3],clearli:1,click:1,client:2,clutter:1,code:[3,4],collaps:[1,2],collect:[2,3,4],collectionadmin:2,collectionpag:2,collections_exact:2,collectionsignalhandl:2,column:[1,2],combin:2,comma:2,command:4,commit:4,commitwithin:2,compar:2,compare_protected_field:2,compil:4,complet:1,compon:1,compress:2,compressor:1,condition:2,conf:3,config:4,configur:[2,3,4],conflict:3,connect:[2,4],consist:1,constitut:0,constrain:1,contain:[0,4],content:[0,2,3,4],content_dir:2,content_typ:2,contentpag:2,context:[1,2],continu:1,contribut:[1,2],contributor:[0,1,2,3],contributorpag:2,control:1,conveni:[2,4],convent:4,convers:2,convert:[2,3],copi:[1,2,3,4],copy_detail:2,copy_last_upd:2,core:[2,3,4],coreadmin:2,correct:1,correctli:1,correspend:2,correspond:[0,2],could:1,count:2,count_pag:2,crawl:4,creat:[1,2,3,4],creation:[1,2],credenti:[1,2],credit:1,csh:4,csv:2,current:[1,2,4],cursor:1,custom:[2,4],data:[2,3,4],data_format:2,data_list:2,databas:[2,3,4],dataset:[2,3],datastor:2,date:[1,2,3],datefield:2,datetim:2,db_obj:2,decid:1,declar:3,decod:2,decompress:2,deconstruct:2,decor:2,defin:2,definit:[1,2],delet:[2,3],delete_pairtree_data:2,deni:2,depend:[1,2,3,4],deploi:[1,4],descript:[0,1,2],design:2,desir:3,detail:[0,1,2],detect:2,determin:2,dev:4,dict:2,dictionari:2,differ:[1,2],differenti:1,digit:[0,1,2,3],digitizedwork:[0,2],digitizedworkadmin:2,digitizedworkbyrecordid:2,digitizedworkcsv:2,digitizedworkdetailview:2,digitizedworklistview:2,directli:4,directori:[2,3,4],disabl:2,discrep:1,dispatch:2,displai:[0,1,2,3],display_label:2,display_titl:2,distinguish:1,distribut:1,div:2,django:[0,1,2,3,4],doc:[2,4],document:1,doe:2,doesn:2,doesnotexist:2,don:1,done:2,download:[1,2],due:3,duplic:1,each:2,easi:1,easier:[1,4],easili:1,edit:[0,1,2],editor:[1,3],editori:1,editorialindexpag:2,editorialpag:2,educ:2,effect:[2,4],effici:1,either:4,elsewher:2,email:3,emploi:0,empti:[2,4],empty_permit:2,enabl:[0,2,3],endpoint:2,engin:1,ensur:[2,4],enter:1,entri:2,enumcron:2,enumer:2,environ:4,equival:2,error:[1,2],error_class:2,errorlist:2,essai:[1,2],eta:2,etc:2,eulxml:2,even:2,everyon:1,everyth:[2,3],exampl:[0,2],except:[1,2],exclud:[1,2],exist:[1,2,3],existing_id:2,expand:[0,2],expect:2,experi:1,expos:2,expres:2,express:2,extend:2,extens:2,f0a326c10b2a6dc9ae5e3ede261c9897:2,face:[1,2],facet:[1,2],facet_rang:2,facetchoicefield:2,fail:1,fall:2,fals:2,favicon:1,featur:1,fetch:2,few:1,field:[0,1,2,3],field_data:2,field_ord:2,file:[2,3,4],file_extens:2,fileid:2,filenam:2,fill:1,filter:2,filter_existing_id:2,find:1,findabl:1,firefox:1,first:[1,2,4],fix:1,fixtur:[1,3,4],flag:2,flow:[1,4],fmt:2,focu:1,focus:1,folder:4,font:1,footer:1,footnot:1,forc:4,form:1,form_class:2,form_valid:2,format:2,formset:2,found:2,fptr:2,frequent:4,fresh:3,from:[0,1,2,3,4],from_db_valu:2,front_cov:2,frontend:4,full:[1,2,3],gener:[0,1,2,4],get:[1,2],get_absolute_url:2,get_aggreg:2,get_context_data:2,get_csv_filenam:2,get_data:2,get_descript:2,get_expand:2,get_facet:2,get_hathi_data:2,get_hathi_id:2,get_highlight:2,get_json:2,get_metadata:2,get_page_highlight:2,get_plaintext_descript:2,get_prep_valu:2,get_queryset:2,get_readonly_field:2,get_redirect_url:2,get_result:2,get_solr_connect:2,get_solr_sort_field:2,get_status_messag:2,get_structur:2,get_success_url:2,get_template_nam:2,get_usag:2,gif:1,git:4,github:[1,4],give:[1,2],given:2,going:1,gone:2,googl:[1,3],graphic:1,group:[0,1,2,3],group_nam:2,gtags_analytics_id:3,haeder:2,handl:1,handle_attr_delet:2,handle_attr_sav:2,handler:2,has:[2,3],has_chang:2,has_fulltext:2,has_keyword_queri:2,hathi:[0,1,3],hathi_data:[2,3],hathi_id:2,hathi_import:[2,3,4],hathibaseapi:2,hathibibliographicapi:2,hathibibliographicrecord:2,hathidataapi:2,hathiimport:2,hathiitemforbidden:2,hathiitemnotfound:2,hathiobject:2,hathitrust:[0,2,3,4],hathitrust_oauth_kei:3,hathitrust_oauth_secret:3,have:[1,2,3],head:1,header:[1,2,3],help:[1,2],help_text:2,here:1,hidden:1,highlight:2,histogram:1,histor:2,histori:1,hit:1,home:2,homepag:[1,2],hot:4,hover:2,how:1,hst:1,htid1:2,htid2:2,htid3:2,htid:2,html00000001:2,html00000496:2,html:[2,4],http:[1,2,3,4],httprespons:2,human:2,iOS:1,icon:2,id_:2,id_typ:2,id_valu:2,idea:1,identifi:[1,2],identify_index_depend:2,ids:2,ignor:[1,2],imag:[1,2],image_on_pag:2,imagewithcapt:2,img00000001:2,implement:[1,2],implicit_page_numb:2,includ:[1,2,3,4],incorrect:1,independ:4,index:[0,1,3,4],index_chunk_s:2,index_data:2,index_depends_on:2,index_id:2,index_item:2,indic:[1,2],individu:[0,1,2],info:2,inform:[1,2],initi:[2,4],initial_valu:2,input:[1,2],insensit:1,insert:[1,2],inspect:2,instal:[2,3,4],instanc:2,instanti:2,institut:2,integ:2,integerfield:2,intend:2,interact:1,interest:1,interfac:1,intern:2,invalid:[1,2],involv:1,is_publ:2,is_suppress:2,isoformat:2,issu:1,item:[0,1,2,3],item_id:2,item_typ:2,iter:2,its:[0,1,2],jasmin:4,javascript:[1,4],json:[1,2,3,4],jsondecodeerror:2,jump:1,just:4,karma:4,keep:[1,2],kei:2,keyboard:1,keyword:[1,2],kind:1,kwarg:2,labeel:2,label:2,label_suffix:2,languag:2,larg:[1,2],last:[1,2,3],last_modifi:2,lastmodifiedlistmixin:2,lastmodifiedmixin:2,later:1,layer:0,layout:1,lazi:1,lead:2,left:2,length:2,level:[0,1,4],lib:3,librari:[1,3,4],like:[1,2],likelihood:1,line:2,link:[1,2],lish:2,lisht:2,list:[1,2,3],list_collect:2,listen:2,load:[1,2,3,4],loaddata:3,local:[0,1,2,3,4],local_block:2,local_set:4,localhost:4,localset:[3,4],localuseradmin:2,locat:2,log:[2,4],log_msg_src:2,logentri:2,logic:[2,3],login:1,logo:1,look:[1,4],lower:1,m2m_chang:2,made:[1,3,4],mai:2,main:[1,3],make:[1,2,4],malform:2,manag:[0,3,4],mani:[1,2],manual:[1,3],map:2,marc:2,marcxml:[1,2],mark:[1,2],master:4,match:[1,2],materi:[0,2,3],max:[1,2],max_length:2,maximum:2,md5:2,meant:1,media:1,member:[1,3],membership:2,memori:4,menu:[1,2],messag:2,met:2,meta_descript:2,meta_titl:2,metadata:[0,1,2,3],metadata_format:2,method:[2,4],metsfiil:2,metsfil:2,metsfile_path:2,mezzanin:[0,1,3],microsecond:2,might:2,migrat:[2,3,4],mileston:1,mimetyp:2,min:[1,2],minim:2,minimalmet:2,minimum:[1,2],minor:1,miss:1,mixin:2,mobil:1,model:0,modelmultiplechoicefield:2,modelmultiplechoicefieldwithempti:2,moder:3,modif:[2,3],modifi:[1,2,3],modul:[0,4],month:2,more:[1,2],most:[1,4],mrc:2,multi:1,multipl:[1,2],multipleobjectsreturn:2,multivalu:2,multivaluefield:2,must:[2,3],mute:1,mysql:1,name:[1,2,3,4],name_chang:2,navig:[1,3],nearli:1,necessarili:2,need:[2,3,4],newer:2,newest:1,newli:2,newlin:2,no_collection_label:2,no_flag:2,node:2,nodelistfield:2,non:[1,2,3],none:[2,3],normal:[1,2],note:[1,2,4],noth:2,now:2,npm:4,number:[1,2],numer:[1,2],oauth:2,obj:2,object:2,objectnotfoundexcept:2,obviou:2,occurr:2,onc:[2,3,4],one:[0,1,2,3],onli:2,open:[1,2],opengraph:1,openrefin:1,opensearchdescriptionview:2,oper:2,option:[0,2,3,4],orcid:2,order:[1,2,3],ordereddict:2,orderlabel:2,org:[2,3],organ:1,origin:2,other:2,otherwis:2,out:[1,2,3],output_result:2,over:[1,2],overrid:[1,2],own:2,pa11i:4,pa11yci:4,packag:2,page:[0,1,3,4],page_count:2,page_group:2,page_index_data:2,pagedsolrqueri:2,pagepreviewdescriptionmixin:2,pagin:[1,2],pairtre:[2,3,4],pairtree_cli:2,pairtree_id:2,pairtree_object:2,pairtree_prefix:2,pairtreestoragecli:2,param:2,paramet:2,parent:2,part:[1,2],particular:[1,2],pass:2,password:1,patch:2,path:[1,2,3,4],path_compon:2,pattern:2,peopl:[1,3],per:2,perform:[1,2],period:1,permiss:[1,2,3],person:[0,2],photo:[0,1,2],pip:4,pipelin:1,place:[1,2],placehold:[1,2],placement:1,plain:2,poetri:2,pointer:2,popul:[1,2,3],populate_field:2,populate_from_bibdata:2,portion:2,posit:1,positivesmallintegerfield:2,possibl:[1,2,4],post:[1,2],post_sav:2,ppa:[0,1,2,3,4],pre:2,pre_delet:2,predefin:3,prefix:[2,3],preliminari:2,present:[2,3],preserv:[0,1,2],prevent:2,preview:[1,2,3],previou:[1,2,3],previous:[1,3],primari:0,princeton:[1,2],print:[1,2],printed_by_r:2,priorit:1,process:[2,4],prod:4,product:[1,4],profil:2,progbar:2,progress:[1,2,3,4],progressbar:2,project:[0,1,2,3,4],project_rol:2,promot:1,properti:[2,3,4],prosodi:[1,2],protect:2,protected_field:[0,2],protectedworkfield:2,protectedworkfieldflag:2,provid:[0,1,2,3,4],provision:[1,4],ptree_client:2,pub:[1,2],pub_dat:2,pub_date_minmax:2,pub_plac:2,public_not:2,publish:[1,2],pull:[1,2,4],pulldown:1,punctuat:1,purpos:[0,2],pymarc:2,pytest:4,python3:4,python:[2,3,4],pythonpath:4,queri:[1,2],query_opt:2,queryset:2,question:2,question_popup_text:2,quickli:1,quot:1,radioselect:2,radioselectwithdis:2,rais:2,rang:[1,2],rangefield:2,rangewidget:2,rather:1,raw:2,raw_respons:2,reactiv:1,read:[2,4],readabl:2,rebuild:4,recent:[1,2,4],recommend:[3,4],recompil:4,record:[1,2,3],record_id:2,redirect:2,reduc:1,refactor:1,refin:1,reflect:2,regular:2,reindex:[2,3],rel:1,relat:[1,2],relationship:2,releas:[1,3,4],relev:1,reload:[1,2,3,4],remov:[0,1,2,3],remove_from_index:2,render:2,render_to_csv:2,repeat:2,repeatedli:2,replac:[1,3],repo:4,report:[0,1,2],repres:0,represent:2,request:[2,3,4],requir:[1,2,3,4],res:1,research:1,reset:2,resolv:1,respond:2,respons:[2,3],restart:3,restrict:2,result:[0,1,2],retriev:[2,3],revis:[0,1,3],rich:0,richtext:2,right:2,role:[1,2],roughli:2,rout:2,row:2,rsync:[2,3,4],run:[2,3,4],runserv:4,same:[2,4],sampl:4,san:1,save:[1,2],save_model:2,save_rel:2,schema:[3,4],scholarli:[1,2],script:[1,2,3],scroll:1,scss:1,search:[0,2,4],search_descript:2,searchabl:2,searchform:2,searchwithinworkform:2,second:2,section:2,secur:1,see:[1,2,3],select:[1,2,3],selectdisabledmixin:2,selectwithdis:2,semant:[1,4],sender:2,sens:1,sep:2,separ:[0,1,2,4],seq:2,sequenc:2,sequenti:1,serif:1,serv:[2,4],server:[3,4],servic:2,session:2,set:[1,2,3,4],set_choices_from_facet:2,set_limit:2,set_url_path:2,setenv:4,setup:4,setup_site_pag:[2,3],sever:1,share:[1,2],should:[1,2,3,4],show:2,shown:2,side:1,signal:2,simpl:2,simpli:4,singl:[0,2],site:[1,3,4],sitemap:[1,4],sitewid:1,size:[1,2],skip:2,slice:2,slug:[2,3],small:4,snippet:[1,2],softwar:1,solconfig:3,sold:2,solr:[1,3,4],solr_conf:[3,4],solr_cor:[3,4],solr_schema:[2,3,4],solr_schema_field:2,solr_schema_field_typ:2,solr_test_cor:4,solr_tim:2,solr_timestamp_to_datetim:2,solrclient:2,solrconfig:3,solrrespons:2,solrschema:2,some:[0,1],someon:2,someth:1,soon:1,sort:[1,2],sort_titl:2,sourc:[1,2,4],source_id:[0,1,2],source_link:2,source_url:2,sourcemap:4,space:1,spec:2,special:1,specif:[1,2,4],specifi:2,specifici:2,sphinx:4,split:2,sql:0,srcid:1,stabl:1,staff:2,staff_member_requir:2,stai:1,standard:2,start:[2,4],stat:2,state:1,statement:1,statist:1,statu:2,status_messag:2,still:2,stock:0,stop:2,storag:2,storage_except:2,store:[2,3],str:2,strict:1,string:2,string_i:2,stringfield:2,strip:2,strong:2,struct:2,structblock:2,structmap:2,structmap_pag:2,structmappag:2,structur:[1,2],stub:3,studi:2,style:[1,4],subclass:[0,2],subcollect:1,submit:1,subsect:2,subtitl:[1,2],subtitle_nostem:2,success:2,successfulli:2,suffici:2,summari:1,suppli:2,support:[0,1,2],suppress:[1,2,3],sure:[3,4],surpress:2,sync:1,system:1,tab:1,tabl:0,tag:[1,2],take:[2,4],taken:2,team:[1,2],technical_contact:3,templat:[1,2],template_nam:2,temporarili:2,term:[1,2],test:1,text:[0,1,2],text_en:2,text_field:2,text_fil:2,text_file_id:2,text_file_loc:2,text_nostem:2,textfield:2,than:[1,2],thei:2,them:[1,2,4],thi:[0,1,2,3,4],thin:0,thing:4,those:[1,2],thousand:2,throttl:1,through:[1,2],thumbnail:1,tile:1,time:[1,2],timefield:2,timelin:1,timestamp:2,titl:[1,2,3],title_nostem:2,to_python:2,togeth:[0,1],tool:[1,2],top:[1,3,4],total:2,touch:2,track:[0,1],trackchangesmodel:2,transport:1,tri:2,trigger:2,tupl:2,tweak:1,twitter:1,two:[0,2,3,4],txt00000001:2,txt:4,type:[0,1,2,3],tzinfo:1,unapiview:2,unavail:2,uncategor:2,under:[0,2,4],understand:1,unformat:1,unifi:1,uninintention:1,unit:4,unneed:1,unsav:2,unset:2,unstem:1,unsuppress:2,unus:1,updat:[2,3],update_solr_schema:2,uri:2,url:[2,3,4],url_path:2,usag:2,use:[1,2,3,4],use_required_attribut:2,used:[1,2],useful:4,user:[2,3],useradmin:2,usernam:1,uses:[0,2,4],using:[0,1,2,4],valid:[1,2],valid_valu:2,valu:2,vari:2,variabl:4,variant:2,variou:0,vary_head:2,vary_on_head:2,varyonheadersmixin:2,verbose_nam:2,version:[0,2,3],via:[1,2,3,4],viabl:1,viaf:2,view:1,viewabl:1,virtualenv:4,visual:1,volum:[1,2],wagtail:[1,2,3],wai:[1,2],wand:1,want:1,web:[2,4],webkit:1,websit:2,well:[0,1,4],were:[1,2,3],what:[1,2],when:[1,2,4],where:[1,2],which:[0,1,2,3],whitespac:2,who:[1,3],wide:1,widget:2,width:2,window:1,winthrop:2,wish:4,within:[1,2],without:[1,2],word:1,work:[0,1,2,3,4],would:1,wrap:2,wrapper:2,write:1,written:4,wrong:1,wrongli:1,www:[2,3],xml:[1,2,3,4],xmlmap:2,xmlobject:2,year:[1,2],yet:2,you:[2,3,4],your:[3,4],zero:3,zipfil:[1,2],zipfile_path:2,zotero:1},titles:["Architecture","CHANGELOG","Code Documentation","Deploy and Upgrade notes","Princeton Prosody Archive documentation"],titleterms:{"export":1,"function":1,"import":[1,2,3],"public":1,admin:[1,2],architectur:0,archiv:[2,4],basic:1,bug:1,bulk:[1,3],changelog:1,chore:1,code:2,collect:[0,1],command:2,common:2,content:1,csv:1,curat:1,data:1,databas:0,deploi:3,design:1,develop:4,document:[2,4],editori:2,filter:[1,3],form:2,hathi:2,hathitrust:1,highlight:[1,3],improv:1,index:2,indic:4,initi:[0,1],instruct:4,launch:1,licens:4,manag:[1,2],materi:1,model:2,note:3,other:1,page:2,princeton:4,prosodi:4,releas:0,schema:[0,2],search:[1,3],setup:2,simpl:[1,3],site:2,soft:1,solr:[0,2],tabl:4,test:4,unapi:2,updat:[0,1],upgrad:3,user:1,util:2,version:1,view:2,wagtail:0}})