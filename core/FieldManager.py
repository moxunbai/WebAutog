
type_addr_map = {}
classname_map_field = {}
field_decl_funcs = []
field_place_funcs = []
field_max_len=100000

def malloc(obj):
    typename = obj.getBaseName()
    if typename not in type_addr_map:
       type_addr_map[typename]={'p':0,'mmap':{}}
    m_props = type_addr_map[typename]
    f_pos =  m_props['p']
    if f_pos <= -1 or f_pos >=  field_max_len:
        return -1
    # obj.fillField( f_pos)
    newp=f_pos+1
    while newp in m_props['mmap']:
        newp+=1
    newp=newp if newp< field_max_len else -1
    m_props['p'] =newp
    return f_pos

def free(obj):
    typename = obj.getBaseName()
    if typename not in type_addr_map:
       return
    m_props = type_addr_map[typename]   
    o_pos = obj.getAddr()  
    if o_pos in m_props['mmap']:
        del m_props['mmap'][o_pos]
        if o_pos < m_props['p']:
            m_props['p']=o_pos

def addFieldDeclare(func):
    field_decl_funcs.append(func)

def addFieldPlaced(func):
    field_place_funcs.append(func)

def fieldsBuilder():
    for f in field_decl_funcs:
        f()

def fieldsPlace():
    for f in field_place_funcs:
        f()

def registFields(name,f):
    classname_map_field[name] =f

def findFieldByName(name):
    return classname_map_field[name] if name in classname_map_field else None