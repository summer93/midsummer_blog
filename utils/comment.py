
content = 1
def comment_tree(comment_list):
    """
    
    :param comment_list: 
    :return: 
    """
    comment_str = "<div class='comment'>"
    for row in comment_list:
        tpl = "<div class='contents'>%s</div><p></p><br>----来自:%s<input type='submit' value='回复'><hr>"%(row['content'],row['user__username'])
        comment_str += tpl
        if row['child']:
            child_str = comment_tree(row['child'])
            comment_str += child_str
    comment_str += "</div>"

    return comment_str