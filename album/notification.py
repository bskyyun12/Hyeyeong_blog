from django.shortcuts import get_object_or_404
from .models import Comment, ImageComment, Notification

def comment_send_notification(request, post, comment, parent_id):
    # check if there is a same kind of notification.
    # if so, delete the other same kind of notification.
    # get all request.user's notifications on this image
    sent_notifies = Notification.objects.filter(post=post, sender=request.user)
    for sent_notify in sent_notifies:
        # if there is a reply,
        if sent_notify.post_comment != None:
            if sent_notify.post_comment.parent:
                # if the reply's comment is same as new comment's parent_id
                if sent_notify.post_comment.parent.id == parent_id:
                    print('')
                    print(f'Same reply kinds!! deleting previous notify....')
                    sent_notify.delete()
                    break
            # if there is a comment, and new comment is not a reply
            elif parent_id == None:
                print('')
                print(f'Same comment kinds!! deleting previous notify....')
                sent_notify.delete()
                break

    # send notification
    # if this is a reply
    if parent_id:
        # get parent_comment
        parent_comment = Comment.objects.get(id=parent_id)
        # if parent_comment.author is not request.user
        if parent_comment.author != request.user:
            Notification.objects.create(
                receiver=parent_comment.author,
                sender=request.user,
                post=comment.post,
                post_comment=comment,
            ).save()
            print(f'Send notify to {parent_comment.author}')


        replies = Comment.objects.filter(parent=parent_id)
        for reply in replies:
            if reply.author != request.user:
                try:
                    get_object_or_404(
                        Notification,
                        receiver=reply.author,
                        sender=request.user,
                        post=comment.post,
                        post_comment=comment,
                    )
                except:
                    Notification.objects.create(
                        receiver=reply.author,
                        sender=request.user,
                        post=comment.post,
                        post_comment=comment,
                    ).save()
                    print(f'Send notify to {reply.author}')


    # if the comment is not a reply.(it's just comment on the post)
    else:
        # send notification to the post.author
        if post.author != request.user:
            Notification.objects.create(
                receiver=post.author,
                sender=request.user,
                post=comment.post,
                post_comment=comment,
            ).save()
            print(f'Send notify to {post.author}')

def imageComment_send_notification(request, image, image_comment, parent_id):

    # check if there is a same kind of notification.
    # if so, delete the other same kind of notification.
    # get all request.user's notifications on this image
    sent_notifies = Notification.objects.filter(image=image, sender=request.user)
    for sent_notify in sent_notifies:
        # if there is a reply,
        if sent_notify.image_comment != None:
            if sent_notify.image_comment.parent:
                # if the reply's comment is same as new comment's parent_id
                if sent_notify.image_comment.parent.id == parent_id:
                    print('')
                    print(f'Same reply kinds!! deleting previous notify....')
                    sent_notify.delete()
                    break
            # if there is a comment, and new comment is not a reply
            elif parent_id == None:
                print('')
                print(f'Same comment kinds!! deleting previous notify....')
                sent_notify.delete()
                break

    # send notification
    # if this is a reply
    if parent_id:
        # get parent_comment
        parent_comment = ImageComment.objects.get(id=parent_id)
        # if parent_comment.author is not request.user
        if parent_comment.author != request.user:
            Notification.objects.create(
                receiver=parent_comment.author,
                sender=request.user,
                image=image_comment.image,
                image_comment=image_comment,
            ).save()
            print('')
            print(1111111111111111111111111111111111111)
            print(f'Send notify to {parent_comment.author}')


        replies = ImageComment.objects.filter(parent=parent_id)
        for reply in replies:
            if reply.author != request.user:
                try:
                    get_object_or_404(
                        Notification,
                        receiver=reply.author,
                        sender=request.user,
                        image=image_comment.image,
                        image_comment=image_comment,
                    )
                except:
                    Notification.objects.create(
                        receiver=reply.author,
                        sender=request.user,
                        image=image_comment.image,
                        image_comment=image_comment,
                    ).save()
                    print('')
                    print(222222222222222222222222222222)
                    print(f'Send notify to {reply.author}')

    else:
        if image.post.author != request.user:
            Notification.objects.create(
                receiver=image.post.author,
                sender=request.user,
                image=image_comment.image,
                image_comment=image_comment,
            ).save()
            print('')
            print(3333333333333333333333333333333333)
            print(f'Send notify to {image.post.author}')
