import xadmin

from operations.models import UserAsk, CourseComments, UserCourse, UserFavorite, UserMessage, Banner


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']
    model_icon = 'fa fa-question-circle'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', "index"]
    search_fields = ['title', 'image', 'url', "index"]
    list_filter = ['title', 'image', 'url', "index"]
    model_icon = 'fa fa-picture-o'


class UserCourseAdmin(object):
    list_display= ['user', 'course', 'add_time']
    search_fields= ['user', 'course']
    list_filter= ['user', 'course', 'add_time']
    model_icon = 'fa fa-map'

    def save_models(self):
        obj = self.new_obj
        if not obj.id:
            obj.save()
            course = obj.course
            course.students += 1
            course.save()


class UserMessageAdmin(object):
    list_display= ['user', 'message', 'has_read', 'add_time']
    search_fields= ['user', 'message', 'has_read']
    list_filter= ['user', 'message', 'has_read', 'add_time']
    model_icon = 'fa fa-commenting'


class CourseCommentsAdmin(object):
    list_display= ['user', 'course', 'comments', 'add_time']
    search_fields= ['user', 'course', 'comments']
    list_filter= ['user', 'course', 'comments', 'add_time']
    model_icon = 'fa fa-comments'


class UserFavoriteAdmin(object):
    list_display= ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields= ['user', 'fav_id', 'fav_type']
    list_filter= ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-heart'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
